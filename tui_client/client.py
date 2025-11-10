"""
WebSocket Game Client for PyMUD-SS13 TUI

Handles communication with the game server via WebSocket.
"""

import asyncio
import json
from typing import Optional, Dict, Any, Callable, TYPE_CHECKING
import websockets
from textual import log

if TYPE_CHECKING:
    from websockets.asyncio.client import ClientConnection


class GameClient:
    """WebSocket client for communicating with the PyMUD-SS13 server."""

    def __init__(self, server_url: str, app):
        self.server_url = server_url
        self.app = app
        self.websocket: Optional[Any] = None  # Type: ClientConnection when connected
        self.connected = False
        self.receive_task: Optional[asyncio.Task] = None

        # Callbacks for different message types
        self.message_handlers: Dict[str, list[Callable]] = {
            "response": [],
            "system": [],
            "error": [],
            "broadcast": [],
            "location": [],
            "inventory": [],
            "map": [],
            "status": [],
        }

        # Store latest game state
        self.current_location: Optional[Dict[str, Any]] = None
        self.current_inventory: Optional[Dict[str, Any]] = None
        self.current_map: Optional[Dict[str, Any]] = None
        self.player_status: Dict[str, Any] = {}

    async def connect(self) -> bool:
        """Connect to the game server."""
        try:
            log(f"Connecting to {self.server_url}...")
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            log("Connected successfully!")

            # Start receiving messages
            self.receive_task = asyncio.create_task(self._receive_messages())

            return True
        except Exception as e:
            log(f"Connection failed: {e}")
            self.connected = False
            return False

    async def disconnect(self):
        """Disconnect from the game server."""
        if self.receive_task:
            self.receive_task.cancel()
            try:
                await self.receive_task
            except asyncio.CancelledError:
                # Expected exception when cancelling the receive task
                pass

        if self.websocket:
            await self.websocket.close()
            self.connected = False
            log("Disconnected from server")

    async def send_command(self, command: str):
        """Send a command to the game server."""
        if not self.websocket or not self.connected:
            log("Not connected to server")
            return

        try:
            message = json.dumps({"type": "command", "command": command})
            await self.websocket.send(message)
            log(f"Sent command: {command}")
        except Exception as e:
            log(f"Error sending command: {e}")
            self.connected = False

    async def _receive_messages(self):
        """Continuously receive messages from the server."""
        if not self.websocket:
            return

        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(data)
                except json.JSONDecodeError:
                    log(f"Invalid JSON received: {message}")
                except Exception as e:
                    log(f"Error handling message: {e}")
        except websockets.exceptions.ConnectionClosed:
            log("Connection closed by server")
            self.connected = False
        except Exception as e:
            log(f"Error in receive loop: {e}")
            self.connected = False

    async def _handle_message(self, data: Dict[str, Any]):
        """Handle incoming messages from the server."""
        message_type = data.get("type", "response")

        # Update state based on message type
        if message_type == "location":
            self.current_location = data
        elif message_type == "inventory":
            self.current_inventory = data
        elif message_type == "map":
            self.current_map = data
        elif message_type in ["door", "atmosphere", "power"]:
            self.player_status[message_type] = data

        # Call registered handlers
        handlers = self.message_handlers.get(message_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                log(f"Error in message handler: {e}")

    def register_handler(self, message_type: str, handler: Callable):
        """Register a callback for a specific message type."""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)

    def unregister_handler(self, message_type: str, handler: Callable):
        """Unregister a callback for a specific message type."""
        if message_type in self.message_handlers:
            try:
                self.message_handlers[message_type].remove(handler)
            except ValueError:
                pass

    def get_location(self) -> Optional[Dict[str, Any]]:
        """Get the current location data."""
        return self.current_location

    def get_inventory(self) -> Optional[Dict[str, Any]]:
        """Get the current inventory data."""
        return self.current_inventory

    def get_map(self) -> Optional[Dict[str, Any]]:
        """Get the current map data."""
        return self.current_map

    def get_status(self, status_type: str) -> Optional[Dict[str, Any]]:
        """Get a specific status value."""
        return self.player_status.get(status_type)
