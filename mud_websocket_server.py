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
import websockets
from mudpy_interface import MudpyInterface
import integration
import engine
from events import publish

# Import command modules individually to ensure handlers are registered
from commands import basic
from commands import movement
from commands import inventory
from commands import system
from commands import interaction
from commands import debug  # This should be disabled in production

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

# Create the integration with the new engine architecture
mud_integration = integration.create_integration(mudpy_interface)

async def handle_client(websocket):
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
            "message": "Welcome to Space Station Alpha - a sci-fi adventure powered by MUDpy SS13!"
        }))
        
        # Start the connection with MUDpy
        mudpy_interface.connect_client(client_id)
        
        # Publish client connected event to create player in the world
        publish("client_connected", client_id=str(client_id))
        
        # Send initial 'look' command through the integration to get room description
        initial_response = mud_integration.process_command(client_id, "look")
        await websocket.send(json.dumps({
            "type": "response",
            "message": initial_response
        }))
        
        # Handle client messages
        async for message in websocket:
            try:
                data = json.loads(message)
                command = data.get('command', '')
                
                logger.debug(f"Received command from client {client_id}: {command}")
                
                # Forward the command to MUDpy through the integration
                response = mud_integration.process_command(client_id, command)
                
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
        
        # Publish client disconnected event
        publish("client_disconnected", client_id=str(client_id))
        
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
    
    # Create a WebSocket server
    server = await websockets.serve(handle_client, host, port)
    
    # Run forever
    await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        logger.info("WebSocket server stopped by user")
