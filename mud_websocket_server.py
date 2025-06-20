#!/usr/bin/env python3
"""
WebSocket server for MUDpy SS13.
This module provides a WebSocket interface to MUDpy SS13, allowing browser-based clients
to connect to the MUD game without requiring a Telnet client.
"""

import asyncio
import json
import logging
import os
import time
from aiohttp import web, WSMsgType
from mudpy_interface import MudpyInterface
import integration
import engine
from events import publish, subscribe
from collections import deque
from systems.power import get_power_system

# Import command modules individually to ensure handlers are registered
from commands import basic
from commands import movement
from commands import inventory
from commands import system
from commands import interaction
from commands import debug  # This should be disabled in production

# Module logger
logger = logging.getLogger(__name__)

# Dictionary to store active client connections
active_clients = {}

# Create an instance of the MudpyInterface
mudpy_interface = MudpyInterface()

# Create the integration with the new engine architecture
mud_integration = integration.create_integration(mudpy_interface)

# ---------------------------------------------------------------------------
# Map generation and broadcast helpers
# ---------------------------------------------------------------------------


def generate_room_map(start_id: str = "start"):
    """Generate a simple coordinate map of rooms based on exits."""
    world = mud_integration.world
    if start_id not in world.rooms:
        if world.rooms:
            start_id = next(iter(world.rooms))
        else:
            return {}

    offsets = {
        "north": (0, -1),
        "south": (0, 1),
        "east": (1, 0),
        "west": (-1, 0),
    }

    positions = {}
    queue = deque([(start_id, (0, 0))])
    visited = set()

    while queue:
        room_id, pos = queue.popleft()
        if room_id in visited:
            continue
        visited.add(room_id)
        positions[room_id] = pos
        room_obj = world.get_object(room_id)
        if not room_obj:
            continue
        room_comp = room_obj.get_component("room")
        if not room_comp:
            continue
        for direction, dest in room_comp.exits.items():
            if dest not in visited and direction in offsets:
                off = offsets[direction]
                queue.append((dest, (pos[0] + off[0], pos[1] + off[1])))

    return positions


def build_map_payload():
    """Build the payload for /map requests."""
    positions = generate_room_map()
    world = mud_integration.world
    rooms = []
    door_states = {}
    hazards = {}
    power = {}

    for room_id, (x, y) in positions.items():
        room_obj = world.get_object(room_id)
        if not room_obj:
            continue
        rooms.append({"id": room_id, "name": room_obj.name, "x": x, "y": y})
        door_comp = room_obj.get_component("door")
        if door_comp:
            door_states[room_id] = door_comp.is_locked
        room_comp = room_obj.get_component("room")
        if room_comp:
            hazards[room_id] = list(room_comp.hazards)

    # Power states
    ps = get_power_system()
    for grid in ps.grids.values():
        for r in grid.rooms:
            power[r] = grid.is_powered

    return {
        "type": "map",
        "rooms": rooms,
        "doors": door_states,
        "hazards": hazards,
        "power": power,
    }


async def broadcast_to_clients(payload: dict) -> None:
    if active_clients:
        await asyncio.gather(
            *[
                client.send_str(json.dumps(payload))
                for client in active_clients.values()
            ]
        )


def _register_event_handlers():
    """Subscribe to game events and forward them to clients."""

    def door_lock_handler(door_id: str, **_):
        asyncio.create_task(
            broadcast_to_clients(
                {"type": "door_status", "door_id": door_id, "locked": True}
            )
        )

    def door_unlock_handler(door_id: str, **_):
        asyncio.create_task(
            broadcast_to_clients(
                {"type": "door_status", "door_id": door_id, "locked": False}
            )
        )

    def atmos_update(room_id: str, atmosphere: dict, hazards: list, **_):
        asyncio.create_task(
            broadcast_to_clients(
                {"type": "atmos_warning", "room_id": room_id, "hazards": hazards}
            )
        )

    def power_update(grid_id: str, is_powered: bool, **kwargs):
        asyncio.create_task(
            broadcast_to_clients(
                {"type": "power_status", "grid_id": grid_id, "is_powered": is_powered}
            )
        )

    def room_power_change(room_id: str, powered: bool, **_):
        name = mud_integration.get_room_name(room_id) or room_id
        msg = (
            f"The lights flicker back on in {name}."
            if powered
            else f"The lights go out in {name}."
        )
        asyncio.create_task(
            broadcast_to_clients({"type": "broadcast", "message": msg})
        )

    def hazard_added(room_id: str, hazard: str, **_):
        name = mud_integration.get_room_name(room_id) or room_id
        h = hazard.replace("_", " ")
        msg = f"Warning: {h} detected in {name}!"
        asyncio.create_task(
            broadcast_to_clients({"type": "broadcast", "message": msg})
        )

    def hazard_removed(room_id: str, hazard: str, **_):
        name = mud_integration.get_room_name(room_id) or room_id
        h = hazard.replace("_", " ")
        msg = f"{h.title()} cleared in {name}."
        asyncio.create_task(
            broadcast_to_clients({"type": "broadcast", "message": msg})
        )

    def hazard_warning(room_id: str, hazard: str, **_):
        name = mud_integration.get_room_name(room_id) or room_id
        h = hazard.replace("_", " ")
        msg = f"Warning: {h} in {name}!"
        asyncio.create_task(
            broadcast_to_clients({"type": "broadcast", "message": msg})
        )

    subscribe("door_locked", door_lock_handler)
    subscribe("door_emergency_lockdown", door_lock_handler)
    subscribe("door_unlocked", door_unlock_handler)
    subscribe("atmos_updated", atmos_update)
    subscribe("power_status_update", power_update)
    subscribe("room_power_changed", room_power_change)
    subscribe("room_hazard_added", hazard_added)
    subscribe("room_hazard_removed", hazard_removed)
    subscribe("hazard_warning", hazard_warning)


_register_event_handlers()


async def handle_client(websocket):
    """
    Handle WebSocket connections from clients.
    Each client connection is given a unique ID and stored in the active_clients dictionary.
    Client messages are processed and forwarded to the MUDpy server.
    Responses from the MUDpy server are sent back to the client.
    """
    # Generate a unique client ID
    client_id = id(websocket)
    logger.info(f"New client connected: {client_id}, type: {type(client_id)}")

    # Register client
    active_clients[client_id] = websocket

    # Log active clients for debugging
    logger.debug(f"Active clients: {list(active_clients.keys())}")

    try:
        # Send welcome message
        await websocket.send_str(
            json.dumps(
                {
                    "type": "system",
                    "message": "Welcome to Space Station Alpha - a sci-fi adventure powered by MUDpy SS13!",
                }
            )
        )

        # Start the connection with MUDpy
        logger.info(f"Connecting client to MUDpy interface: {client_id}")
        mudpy_interface.connect_client(client_id)

        # Debug client session state
        logger.debug(
            f"After connect_client, player_locations: {mudpy_interface.player_locations}"
        )
        logger.debug(
            f"After connect_client, client_sessions: {mudpy_interface.client_sessions}"
        )

        # Publish client connected event to create player in the world
        # Note: We keep the client_id as an integer throughout the system
        logger.info(f"Publishing client_connected event for: {client_id}")
        publish("client_connected", client_id=client_id)

        try:
            # Send initial 'look' command through the integration to get room description
            logger.info(f"Sending initial 'look' command for client: {client_id}")
            initial_response = mud_integration.process_command(client_id, "look")

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
            await websocket.send_str(
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
        except Exception as e:
            logger.error(f"Error processing initial look command: {e}")
            await websocket.send_str(
                json.dumps(
                    {
                        "type": "error",
                        "message": "Error initializing game state. Please refresh and try again.",
                    }
                )
            )

        # Handle client messages
        async for msg in websocket:
            if msg.type == WSMsgType.TEXT:
                try:
                    message = msg.data
                    # Try to parse JSON, but also handle plain text
                    try:
                        data = json.loads(message)
                        if data.get("type") == "map_request":
                            await websocket.send_str(json.dumps(build_map_payload()))
                            continue
                        if data.get("type") == "inventory_request":
                            inv = mudpy_interface.get_inventory_data(client_id)
                            await websocket.send_str(
                                json.dumps({"type": "inventory", "inventory": inv})
                            )
                            continue
                        if data.get("type") == "object_request":
                            obj = mud_integration.get_object_data(data.get("object_id", ""))
                            await websocket.send_str(
                                json.dumps({"type": "object_data", "object": obj})
                            )
                            continue
                        command = data.get("command", "")
                    except json.JSONDecodeError:
                        # If not valid JSON, treat the entire message as a command
                        command = message
                        logger.debug(
                            f"Received plain text command from client {client_id}: {command}"
                        )

                    # Forward the command to MUDpy through the integration
                    if command:
                        if command.strip() == "/map":
                            await websocket.send_str(json.dumps(build_map_payload()))
                        else:
                            logger.debug(
                                f"Processing command from client {client_id}: {command}"
                            )
                            response = mud_integration.process_command(
                                client_id, command
                            )

                            # Send the response back to the client
                            await websocket.send_str(
                                json.dumps({"type": "response", "message": response})
                            )
                    else:
                        logger.warning(
                            f"Empty command received from client {client_id}"
                        )
                        await websocket.send_str(
                            json.dumps(
                                {"type": "error", "message": "Please enter a command."}
                            )
                        )

                except Exception as e:
                    logger.error(
                        f"Error processing message from client {client_id}: {str(e)}"
                    )
                    await websocket.send_str(
                        json.dumps(
                            {
                                "type": "error",
                                "message": "Error processing your command. Please try again.",
                            }
                        )
                    )
            elif msg.type == WSMsgType.ERROR:
                logger.error(
                    f"WebSocket connection closed with exception: {websocket.exception()}"
                )
            elif msg.type == WSMsgType.CLOSE:
                logger.info(f"WebSocket connection closed by client")
                break

    except Exception as e:
        logger.error(f"Connection error: {e}")

    finally:
        # Clean up client connection
        if client_id in active_clients:
            del active_clients[client_id]

        # Publish client disconnected event
        # Keep client_id as an integer for consistency
        logger.info(f"Client disconnected: {client_id}")
        publish("client_disconnected", client_id=client_id)

        # Disconnect from MUDpy
        mudpy_interface.disconnect_client(client_id)

        return websocket


async def broadcast_message(message):
    """
    Broadcast a message to all connected clients.

    Args:
        message (str): The message to broadcast.
    """
    if active_clients:
        await asyncio.gather(
            *[
                client.send_str(json.dumps({"type": "broadcast", "message": message}))
                for client in active_clients.values()
            ]
        )


# The WebSocket server is now handled in start_server.py using aiohttp

if __name__ == "__main__":
    logger.warning(
        "This module should be imported by start_server.py, not run directly."
    )
