#!/usr/bin/env python3
"""
MUD Server module for Space Station 13 MUD.
This module provides a WebSocket server for the MUD game that handles client connections,
authentication, and dispatches commands to the game engine.
"""

import asyncio
import json
import logging
import os
import yaml
from typing import Dict, List, Callable, Any, Optional, Set, Coroutine
import account_system as accounts
import websockets
from websockets.asyncio.server import serve
from mudpy_interface import MudpyInterface
import integration
import engine
from events import publish, subscribe, unsubscribe
from systems.jobs import JOB_SYSTEM
import world

# Module logger
logger = logging.getLogger(__name__)


class MudServer:
    """
    WebSocket server for the Space Station 13 MUD.

    This class handles WebSocket connections, player authentication,
    and dispatches commands to the game engine.
    """

    def __init__(
        self, host: str = "0.0.0.0", port: int = 5000, config_path: str = "config.yaml"
    ):
        """
        Initialize the MUD Server.

        Args:
            host (str): Host address to bind to. Defaults to '0.0.0.0'.
            port (int): Port to listen on. Defaults to 5000.
            config_path (str): Path to the configuration file. Defaults to 'config.yaml'.
        """
        # Load config if it exists
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            self.host = config.get("host", host)
            self.port = config.get("port", port)
        else:
            self.host = host
            self.port = port

        # Initialize MUDpy interface
        self.mudpy_interface = MudpyInterface(config_path)

        # Create integration with the new engine architecture
        self.mud_integration = integration.create_integration(self.mudpy_interface)

        # Track active sessions: WebSocket -> client_id mapping
        self.sessions: Dict[Any, int] = {}

        # Register for events
        self._register_event_handlers()

        logger.info(f"MUD Server initialized on {self.host}:{self.port}")

    def _register_event_handlers(self) -> None:
        """Subscribe server callbacks to global events."""
        subscribe("player_moved", self._on_player_moved)
        subscribe("item_taken", self._on_item_taken)
        subscribe("item_dropped", self._on_item_dropped)
        subscribe("item_used", self._on_item_used)
        subscribe("player_said", self._on_player_said)
        subscribe("npc_said", self._on_npc_said)

    def _unregister_event_handlers(self) -> None:
        """Remove server callbacks from the event system."""
        unsubscribe("player_moved", self._on_player_moved)
        unsubscribe("item_taken", self._on_item_taken)
        unsubscribe("item_dropped", self._on_item_dropped)
        unsubscribe("item_used", self._on_item_used)
        unsubscribe("player_said", self._on_player_said)
        unsubscribe("npc_said", self._on_npc_said)

    def __del__(self) -> None:
        self._unregister_event_handlers()

    async def handler(self, websocket, path: str) -> None:
        """
        Handle a client WebSocket connection.

        Args:
            websocket: The WebSocket connection.
            path: The connection path.
        """
        client_id = await self._login(websocket)

        try:
            logger.info(f"Handling client: {client_id}")
            # Handle client messages
            async for message in websocket:
                try:
                    # Parse the message
                    try:
                        data = json.loads(message)
                        command = data.get("command", "")
                    except json.JSONDecodeError:
                        # If not JSON, treat as plain command
                        command = message.strip()

                    # Process the command
                    if command:
                        logger.debug(
                            f"Processing command from client {client_id}: {command}"
                        )
                        response = self.mud_integration.process_command(
                            client_id, command
                        )

                        # Send response back to client
                        await websocket.send(
                            json.dumps({"type": "response", "message": response})
                        )
                    else:
                        logger.warning(
                            f"Empty command received from client {client_id}"
                        )
                        await websocket.send(
                            json.dumps(
                                {"type": "error", "message": "Please enter a command."}
                            )
                        )

                except Exception as e:
                    logger.error(
                        f"Error processing command from client {client_id}: {e}"
                    )
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "error",
                                "message": f"Error processing your command: {str(e)}",
                            }
                        )
                    )

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed for client {client_id}")
        except Exception as e:
            logger.error(f"Unexpected error for client {client_id}: {e}")
        finally:
            await self._logout(websocket, client_id)

    async def _login(self, websocket) -> int:
        """
        Handle client login process.

        Args:
            websocket: The WebSocket connection.

        Returns:
            int: The client ID.
        """
        # Generate a unique client ID
        client_id = id(websocket)

        # Add to sessions
        self.sessions[websocket] = client_id

        # Send welcome message
        await websocket.send(
            json.dumps(
                {
                    "type": "system",
                    "message": "Welcome to Space Station Alpha - a sci-fi adventure powered by MUDpy SS13!",
                }
            )
        )

        # Prompt for account credentials
        await websocket.send(json.dumps({"type": "system", "message": "Username:"}))
        try:
            name_msg = await websocket.recv()
            try:
                data = json.loads(name_msg)
                username = data.get("command", name_msg).strip()
            except json.JSONDecodeError:
                username = name_msg.strip()
        except Exception:
            username = "guest"

        await websocket.send(json.dumps({"type": "system", "message": "Password:"}))
        try:
            pass_msg = await websocket.recv()
            try:
                data = json.loads(pass_msg)
                password = data.get("command", pass_msg).strip()
            except json.JSONDecodeError:
                password = pass_msg.strip()
        except Exception:
            password = ""

        if not accounts.authenticate(username, password):
            if username not in accounts._load():
                accounts.create_account(username, password, admin=username == "admin")
            else:
                await websocket.send(json.dumps({"type": "error", "message": "Invalid password."}))
                raise websockets.exceptions.ConnectionClosed(1000, "bad credentials")

        is_admin = accounts.is_admin(username)

        # Check if this account already has a character
        character = accounts.get_character(username)

        # Connect client to MUDpy interface
        logger.info(f"Connecting client to MUDpy interface: {client_id}")
        self.mudpy_interface.connect_client(client_id, username=username, is_admin=is_admin)

        # Publish client connected event to create player in the world
        logger.info(f"Publishing client_connected event for: {client_id}")
        publish("client_connected", client_id=client_id)

        # Let the player know they are on the shuttle heading to the station
        await websocket.send(
            json.dumps(
                {
                    "type": "system",
                    "message": (
                        "You strap into the arrival shuttle as it approaches "
                        "Space Station Alpha."
                    ),
                }
            )
        )

        try:
            # Send initial 'look' command to get room description
            logger.info(f"Sending initial 'look' command for client: {client_id}")
            initial_response = self.mud_integration.process_command(client_id, "look")

            # Safer logging of responses
            if initial_response:
                trimmed_response = (
                    initial_response[:50] + "..."
                    if len(initial_response) > 50
                    else initial_response
                )
                logger.info(f"Received initial response: {trimmed_response}")
            else:
                logger.info("Received empty initial response")

            # Send response back to client
            await websocket.send(
                json.dumps(
                    {
                        "type": "response",
                        "message": (
                            initial_response
                            if initial_response
                            else "Welcome! You find yourself in a mysterious location."
                        ),
                    }
                )
            )
            if not character:
                # Character creation flow
                job_list = ", ".join(sorted(j.job_id for j in JOB_SYSTEM.get_all_jobs()))
                await websocket.send(
                    json.dumps(
                        {
                            "type": "system",
                            "message": (
                                "The shuttle is about to dock. Choose your job "
                                f"({job_list}) to receive your equipment:"
                            ),
                        }
                    )
                )
                try:
                    selection_msg = await websocket.recv()
                    try:
                        sel_data = json.loads(selection_msg)
                        selection = sel_data.get("command", selection_msg).strip()
                    except json.JSONDecodeError:
                        selection = selection_msg.strip()
                except Exception:
                    selection = "assistant"
                if selection not in JOB_SYSTEM.jobs:
                    selection = "assistant"
                await websocket.send(json.dumps({"type": "system", "message": "Choose a name for your character:"}))
                try:
                    name_msg = await websocket.recv()
                    try:
                        ndata = json.loads(name_msg)
                        char_name = ndata.get("command", name_msg).strip()
                    except json.JSONDecodeError:
                        char_name = name_msg.strip()
                except Exception:
                    char_name = f"Crew Member {client_id % 1000}"
                character = {"job": selection, "name": char_name}
                accounts.set_character(username, character)
            job_id = character.get("job", "assistant")
            job = JOB_SYSTEM.assign_job(f"player_{client_id}", job_id)
            if job:
                JOB_SYSTEM.setup_player_for_job(
                    f"player_{client_id}", f"player_{client_id}"
                )
                world_instance = world.get_world()
                p_obj = world_instance.get_object(f"player_{client_id}")
                if p_obj:
                    p_obj.name = character.get("name", p_obj.name)
                spawn_name = (
                    self.mudpy_interface.get_room_name(job.spawn_location)
                    if job.spawn_location
                    else "the station"
                )
                await websocket.send(
                    json.dumps(
                        {
                            "type": "system",
                            "message": (
                                f"You are assigned the role of {job.title}. "
                                f"{job.description} The shuttle docks and you step into {spawn_name}."
                            ),
                        }
                    )
                )
        except Exception as e:
            logger.error(f"Error processing initial look command: {e}")
            await websocket.send(
                json.dumps(
                    {
                        "type": "error",
                        "message": "Error initializing game state. Please refresh and try again.",
                    }
                )
            )

        # Announce new player to other clients
        await self._broadcast(
            f"* A new crew member has boarded the station.", exclude_client=client_id
        )

        return client_id

    async def _logout(self, websocket, client_id: int) -> None:
        """
        Handle client logout process.

        Args:
            websocket: The WebSocket connection.
            client_id: The client ID.
        """
        # Remove from sessions
        if websocket in self.sessions:
            del self.sessions[websocket]
        if not self.sessions:
            self._unregister_event_handlers()

        # Publish client disconnected event
        logger.info(f"Client disconnected: {client_id}")
        publish("client_disconnected", client_id=client_id)

        # Disconnect from MUDpy
        self.mudpy_interface.disconnect_client(client_id)

        # Announce departure to other clients
        await self._broadcast(
            f"* A crew member has left the station.", exclude_client=client_id
        )

    async def _broadcast(
        self, message: str, exclude_client: Optional[int] = None
    ) -> None:
        """
        Broadcast a message to all connected clients.

        Args:
            message: The message to broadcast.
            exclude_client: Optional client ID to exclude from the broadcast.
        """
        for ws, client_id in self.sessions.items():
            if exclude_client is None or client_id != exclude_client:
                try:
                    await ws.send(json.dumps({"type": "broadcast", "message": message}))
                except Exception as e:
                    logger.error(f"Error broadcasting to client {client_id}: {e}")

    # Event handlers
    async def _on_player_moved(
        self, player_id: int, from_location: str, to_location: str
    ) -> None:
        """
        Handle player movement events.

        Args:
            player_id: The player ID.
            from_location: The previous location ID.
            to_location: The new location ID.
        """
        # Get player name
        player_name = f"Crew Member {player_id % 1000}"

        # Get location names
        from_name = self.mudpy_interface.get_room_name(from_location) or from_location
        to_name = self.mudpy_interface.get_room_name(to_location) or to_location

        # Broadcast to players in the same locations
        for ws, client_id in self.sessions.items():
            try:
                client_location = self.mudpy_interface.get_player_location(client_id)

                if client_id != player_id:
                    if client_location == from_location:
                        await ws.send(
                            json.dumps(
                                {
                                    "type": "location",
                                    "message": f"* {player_name} has left to {to_name}.",
                                }
                            )
                        )
                    elif client_location == to_location:
                        await ws.send(
                            json.dumps(
                                {
                                    "type": "location",
                                    "message": f"* {player_name} has arrived from {from_name}.",
                                }
                            )
                        )
            except Exception as e:
                logger.error(
                    f"Error sending movement notification to client {client_id}: {e}"
                )

    async def _on_item_taken(self, item_id: str, player_id: int) -> None:
        """
        Handle item taken events.

        Args:
            item_id: The item ID.
            player_id: The player ID.
        """
        # Get player name and location
        player_name = f"Crew Member {player_id % 1000}"
        player_location = self.mudpy_interface.get_player_location(player_id)

        # Get item name
        item_name = self.mudpy_interface.get_item_name(item_id) or item_id

        # Broadcast to players in the same location
        for ws, client_id in self.sessions.items():
            if (
                client_id != player_id
                and self.mudpy_interface.get_player_location(client_id)
                == player_location
            ):
                try:
                    await ws.send(
                        json.dumps(
                            {
                                "type": "location",
                                "message": f"* {player_name} picks up {item_name}.",
                            }
                        )
                    )
                except Exception as e:
                    logger.error(
                        f"Error sending item taken notification to client {client_id}: {e}"
                    )

    async def _on_item_dropped(self, item_id: str, player_id: int) -> None:
        """
        Handle item dropped events.

        Args:
            item_id: The item ID.
            player_id: The player ID.
        """
        # Get player name and location
        player_name = f"Crew Member {player_id % 1000}"
        player_location = self.mudpy_interface.get_player_location(player_id)

        # Get item name
        item_name = self.mudpy_interface.get_item_name(item_id) or item_id

        # Broadcast to players in the same location
        for ws, client_id in self.sessions.items():
            if (
                client_id != player_id
                and self.mudpy_interface.get_player_location(client_id)
                == player_location
            ):
                try:
                    await ws.send(
                        json.dumps(
                            {
                                "type": "location",
                                "message": f"* {player_name} drops {item_name}.",
                            }
                        )
                    )
                except Exception as e:
                    logger.error(
                        f"Error sending item dropped notification to client {client_id}: {e}"
                    )

    async def _on_item_used(self, item_id: str, player_id: int, item_type: str) -> None:
        """
        Handle item used events.

        Args:
            item_id: The item ID.
            player_id: The player ID.
            item_type: The type of item.
        """
        # Get player name and location
        player_name = f"Crew Member {player_id % 1000}"
        player_location = self.mudpy_interface.get_player_location(player_id)

        # Get item name
        item_name = self.mudpy_interface.get_item_name(item_id) or item_id

        # Broadcast to players in the same location
        for ws, client_id in self.sessions.items():
            if (
                client_id != player_id
                and self.mudpy_interface.get_player_location(client_id)
                == player_location
            ):
                try:
                    await ws.send(
                        json.dumps(
                            {
                                "type": "location",
                                "message": f"* {player_name} uses {item_name}.",
                            }
                        )
                    )
                except Exception as e:
                    logger.error(
                        f"Error sending item used notification to client {client_id}: {e}"
                    )

    async def _on_player_said(
        self, client_id: int, location: str, message: str
    ) -> None:
        """
        Handle player communication events.

        Args:
            client_id: The client ID.
            location: The location.
            message: The message.
        """
        # Get player name
        player_name = f"Crew Member {client_id % 1000}"

        # Broadcast to players in the same location
        for ws, other_client_id in self.sessions.items():
            if (
                other_client_id != client_id
                and self.mudpy_interface.get_player_location(other_client_id)
                == location
            ):
                try:
                    await ws.send(
                        json.dumps(
                            {
                                "type": "chat",
                                "message": f"{player_name} says: {message}",
                            }
                        )
                    )
                except Exception as e:
                    logger.error(
                        f"Error sending chat notification to client {other_client_id}: {e}"
                    )

    async def _on_npc_said(
        self, npc_id: str, location: str, message: str, name: str
    ) -> None:
        """Handle NPC chat events."""
        for ws, other_client_id in self.sessions.items():
            if self.mudpy_interface.get_player_location(other_client_id) == location:
                try:
                    await ws.send(
                        json.dumps(
                            {"type": "chat", "message": f"{name} says: {message}"}
                        )
                    )
                except Exception as e:
                    logger.error(
                        f"Error sending NPC chat to client {other_client_id}: {e}"
                    )

    async def run(self) -> None:
        """
        Run the WebSocket server.
        """
        logger.info(f"Starting MUD server on {self.host}:{self.port}")

        async with serve(self.handler, self.host, self.port, path="/ws") as server:
            # Keep the server running until interrupted
            await asyncio.Future()  # Run forever


def create_mud_server(
    host: str = "0.0.0.0", port: int = 5000, config_path: str = "config.yaml"
) -> MudServer:
    """
    Create a new MUD server instance.

    Args:
        host: Host address to bind to. Defaults to '0.0.0.0'.
        port: Port to listen on. Defaults to 5000.
        config_path: Path to the configuration file. Defaults to 'config.yaml'.

    Returns:
        MudServer: The MUD server instance.
    """
    return MudServer(host, port, config_path)


# For direct execution
if __name__ == "__main__":
    try:
        server = create_mud_server()
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
