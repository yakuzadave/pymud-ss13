#!/usr/bin/env python3
"""
WebSocket server for MUDpy.
This module provides a WebSocket interface to MUDpy, allowing browser-based clients
to connect to the MUD game without requiring a Telnet client.
"""

import asyncio
import json
import logging
import os
import websockets
from mudpy_interface import MudpyInterface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mud_websocket_server')

# Dictionary to store active client connections
active_clients = {}

# Create an instance of the MudpyInterface
mudpy_interface = MudpyInterface()

async def handle_client(websocket, path):
    """
    Handle WebSocket connections from clients.
    Each client connection is given a unique ID and stored in the active_clients dictionary.
    Client messages are processed and forwarded to the MUDpy server.
    Responses from the MUDpy server are sent back to the client.
    """
    # Generate a unique client ID
    client_id = id(websocket)
    logger.info(f"New client connected: {client_id}")
    
    # Register client
    active_clients[client_id] = websocket
    
    try:
        # Send welcome message
        await websocket.send(json.dumps({
            "type": "system",
            "message": "Welcome to MUDpy WebSocket Interface!"
        }))
        
        # Start the connection with MUDpy
        mudpy_interface.connect_client(client_id)
        
        # Handle client messages
        async for message in websocket:
            try:
                data = json.loads(message)
                command = data.get('command', '')
                
                logger.debug(f"Received command from client {client_id}: {command}")
                
                # Forward the command to MUDpy
                response = mudpy_interface.process_command(client_id, command)
                
                # Send the response back to the client
                await websocket.send(json.dumps({
                    "type": "response",
                    "message": response
                }))
                
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received from client {client_id}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid command format. Please send valid JSON."
                }))
    
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client disconnected: {client_id}")
    
    finally:
        # Clean up client connection
        if client_id in active_clients:
            del active_clients[client_id]
        
        # Disconnect from MUDpy
        mudpy_interface.disconnect_client(client_id)

async def broadcast_message(message):
    """
    Broadcast a message to all connected clients.
    
    Args:
        message (str): The message to broadcast.
    """
    if active_clients:
        await asyncio.gather(
            *[client.send(json.dumps({
                "type": "broadcast",
                "message": message
            })) for client in active_clients.values()]
        )

async def start_websocket_server():
    """
    Start the WebSocket server.
    """
    host = '0.0.0.0'
    port = 8000
    
    logger.info(f"Starting WebSocket server on {host}:{port}")
    
    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        logger.info("WebSocket server stopped by user")
