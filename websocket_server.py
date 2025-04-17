#!/usr/bin/env python3
import asyncio
import websockets
import json
import logging
from mudpy_api import MudpyClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('websocket_server')

# Store active connections
active_connections = {}

async def handle_connection(websocket, path):
    """Handle WebSocket connections from clients."""
    # Generate a unique client ID
    client_id = id(websocket)
    logger.info(f"New connection established: {client_id}")
    
    # Create a new Mudpy client for this connection
    mudpy_client = MudpyClient()
    active_connections[client_id] = {
        'websocket': websocket,
        'mudpy_client': mudpy_client
    }
    
    # Send welcome message
    welcome_message = mudpy_client.get_welcome_message()
    await websocket.send(json.dumps({
        'type': 'message',
        'content': welcome_message
    }))
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                command = data.get('command', '')
                
                if command:
                    # Process command through Mudpy
                    response = mudpy_client.process_command(command)
                    
                    # Send response back to client
                    await websocket.send(json.dumps({
                        'type': 'message',
                        'content': response
                    }))
                    
                    logger.debug(f"Command processed for {client_id}: {command}")
            except json.JSONDecodeError:
                # Handle plain text commands (fallback)
                response = mudpy_client.process_command(message)
                await websocket.send(json.dumps({
                    'type': 'message',
                    'content': response
                }))
                logger.debug(f"Plain text command processed for {client_id}: {message}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Connection closed: {client_id}")
    finally:
        # Clean up connection
        if client_id in active_connections:
            active_connections[client_id]['mudpy_client'].close()
            del active_connections[client_id]
            logger.info(f"Connection removed: {client_id}")

async def start_server():
    """Start the WebSocket server."""
    server = await websockets.serve(
        handle_connection,
        '0.0.0.0',  # Listen on all interfaces
        8000        # Port for WebSocket connections
    )
    
    logger.info("WebSocket server started on ws://0.0.0.0:8000")
    await server.wait_closed()

def start_websocket_server():
    """Start the WebSocket server in the current thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server())
    loop.run_forever()

if __name__ == "__main__":
    # Run the server directly if this script is executed
    start_websocket_server()
