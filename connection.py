"""
Connection manager for MUDpy SS13.
This module provides a connection manager for WebSocket connections.
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, Optional, Callable, Coroutine
from fastapi import WebSocket

# Configure logging
logger = logging.getLogger(__name__)

class ConnectionManager:
    """
    WebSocket connection manager.
    
    This class manages WebSocket connections and provides methods for sending
    messages to individual clients or broadcasting to all clients.
    """
    
    def __init__(self):
        """Initialize the connection manager."""
        # Store active connections: WebSocket -> Client ID
        self.active_connections: Dict[WebSocket, str] = {}
        # Store message queues for each connection: WebSocket -> Queue
        self.queues: Dict[WebSocket, asyncio.Queue] = {}
        # Store send tasks for each connection: WebSocket -> Task
        self.tasks: Dict[WebSocket, asyncio.Task] = {}
        
        logger.info("Connection manager initialized")
    
    async def connect(self, websocket: WebSocket) -> str:
        """
        Connect a WebSocket client.
        
        Args:
            websocket: The WebSocket connection.
            
        Returns:
            str: The client ID assigned to this connection.
        """
        # Accept the connection
        await websocket.accept()
        
        # Generate a unique client ID
        client_id = str(uuid.uuid4())
        
        # Store the connection
        self.active_connections[websocket] = client_id
        
        # Create a message queue for this connection
        queue = asyncio.Queue()
        self.queues[websocket] = queue
        
        # Start a background task to send messages to this client
        task = asyncio.create_task(self._sender(websocket, queue))
        self.tasks[websocket] = task
        
        logger.info(f"Client connected: {client_id}")
        
        return client_id
    
    def disconnect(self, websocket: WebSocket) -> Optional[str]:
        """
        Disconnect a WebSocket client.
        
        Args:
            websocket: The WebSocket connection.
            
        Returns:
            Optional[str]: The client ID that was disconnected, or None if not found.
        """
        # Get the client ID
        client_id = self.active_connections.pop(websocket, None)
        
        if client_id:
            # Cancel the send task
            if websocket in self.tasks:
                self.tasks[websocket].cancel()
                del self.tasks[websocket]
            
            # Clean up the queue
            if websocket in self.queues:
                del self.queues[websocket]
            
            logger.info(f"Client disconnected: {client_id}")
        
        return client_id
    
    async def send_personal_message(self, message: Any, websocket: WebSocket) -> None:
        """
        Send a message to a specific client.
        
        Args:
            message: The message to send. If not a string, it will be JSON-encoded.
            websocket: The WebSocket connection to send to.
        """
        if websocket not in self.queues:
            logger.warning(f"Trying to send message to non-existent client")
            return
        
        # Convert message to string if it's not already
        if not isinstance(message, str):
            message = json.dumps(message)
        
        # Add message to the client's queue
        await self.queues[websocket].put(message)
    
    async def broadcast(self, message: Any, exclude: Optional[WebSocket] = None) -> None:
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: The message to broadcast. If not a string, it will be JSON-encoded.
            exclude: Optional WebSocket connection to exclude from the broadcast.
        """
        # Convert message to string if it's not already
        if not isinstance(message, str):
            message = json.dumps(message)
        
        # Queue the message for each client
        for websocket, queue in self.queues.items():
            if exclude is None or websocket != exclude:
                await queue.put(message)
    
    async def broadcast_to_room(self, message: Any, room: str, client_locations: Dict[str, str], exclude_client: Optional[str] = None) -> None:
        """
        Broadcast a message to all clients in a specific room.
        
        Args:
            message: The message to broadcast. If not a string, it will be JSON-encoded.
            room: The room ID to broadcast to.
            client_locations: Mapping of client IDs to room IDs.
            exclude_client: Optional client ID to exclude from the broadcast.
        """
        # Convert message to string if it's not already
        if not isinstance(message, str):
            message = json.dumps(message)
        
        # Find all clients in the specified room
        for websocket, client_id in self.active_connections.items():
            # Skip excluded client
            if exclude_client and client_id == exclude_client:
                continue
            
            # Check if client is in the specified room
            if client_id in client_locations and client_locations[client_id] == room:
                # Queue the message for this client
                await self.queues[websocket].put(message)
    
    async def _sender(self, websocket: WebSocket, queue: asyncio.Queue) -> None:
        """
        Background task to send messages from the queue to a WebSocket client.
        
        Args:
            websocket: The WebSocket connection.
            queue: The message queue for this connection.
        """
        try:
            while True:
                # Wait for a message in the queue
                message = await queue.get()
                
                # Send the message
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending message to client: {e}")
                    # Break out of the loop on error
                    break
                
                # Mark the message as done
                queue.task_done()
        except asyncio.CancelledError:
            # Task was cancelled, exit cleanly
            logger.debug(f"Sender task cancelled for client {self.active_connections.get(websocket, 'unknown')}")
        except Exception as e:
            # Unexpected error
            logger.error(f"Unexpected error in sender task: {e}")
