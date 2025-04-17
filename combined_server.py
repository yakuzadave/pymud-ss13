#!/usr/bin/env python3
"""
Combined HTTP and WebSocket server for MUDpy SS13.
This module provides both HTTP and WebSocket servers on a single port.
"""

import asyncio
import json
import logging
import os
import signal
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import websockets
from websockets.server import WebSocketServerProtocol
from mudpy_interface import MudpyInterface
import integration
import engine
from events import publish, subscribe

# Import command modules to ensure handlers are registered
from commands import basic, movement, inventory, system, interaction

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('combined_server')

# MUDpy interface instance
mudpy_interface = None

# Create integration with the new engine architecture
mud_integration = None

# Dictionary to store active client connections
active_clients = {}

# HTTP server for the web client
class WebClientHandler(SimpleHTTPRequestHandler):
    """
    HTTP request handler for serving the web client.
    Serves files from the web_client directory.
    """
    def __init__(self, *args, **kwargs):
        # Set the directory to the web_client folder
        super().__init__(*args, directory='web_client', **kwargs)

    def log_message(self, format, *args):
        # Custom logging to redirect HTTP logs to our logger
        logger.info(format % args)

def start_http_server():
    """
    Start an HTTP server for the web client.
    This runs in a separate thread.
    """
    host = '0.0.0.0'
    port = 5000
    
    logger.info(f"Starting HTTP server for web client on {host}:{port}")
    
    httpd = HTTPServer((host, port), WebClientHandler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("HTTP server stopped by user")
    finally:
        httpd.server_close()

async def handle_client(websocket):
    """
    Handle a client WebSocket connection.
    
    This function is called for each new WebSocket connection.
    It handles client messages and dispatches them to the MUDpy interface.
    
    Args:
        websocket: The WebSocket connection.
    """
    # Generate a unique client ID
    client_id = id(websocket)
    logger.info(f"New client connected: {client_id}")
    
    # Add to active clients
    active_clients[client_id] = websocket
    
    # Log active clients for debugging
    logger.debug(f"Active clients: {list(active_clients.keys())}")
    
    try:
        # Send welcome message
        await websocket.send(json.dumps({
            "type": "system",
            "message": "Welcome to Space Station Alpha - a sci-fi adventure powered by MUDpy SS13!"
        }))
        
        # Connect client to MUDpy interface
        logger.info(f"Connecting client to MUDpy interface: {client_id}")
        mudpy_interface.connect_client(client_id)
        
        # Debug client session state
        logger.debug(f"After connect_client, player_locations: {mudpy_interface.player_locations}")
        logger.debug(f"After connect_client, client_sessions: {mudpy_interface.client_sessions}")
        
        # Publish client connected event to create player in the world
        logger.info(f"Publishing client_connected event for: {client_id}")
        publish("client_connected", client_id=client_id)
        
        try:
            # Send initial 'look' command to get room description
            logger.info(f"Sending initial 'look' command for client: {client_id}")
            initial_response = mud_integration.process_command(client_id, "look")
            
            # Safer logging of responses
            if initial_response:
                trimmed_response = initial_response[:50] + "..." if len(initial_response) > 50 else initial_response
                logger.info(f"Received initial response: {trimmed_response}")
            else:
                logger.info("Received empty initial response")
            
            # Send response back to client
            await websocket.send(json.dumps({
                "type": "response",
                "message": initial_response if initial_response else "Welcome! You find yourself in a mysterious location."
            }))
        except Exception as e:
            logger.error(f"Error processing initial look command: {e}")
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Error initializing game state. Please refresh and try again."
            }))
        
        # Announce new player to other clients
        await broadcast_message(
            f"* A new crew member has boarded the station.",
            exclude_client=client_id
        )
        
        # Handle messages from this client
        async for message in websocket:
            try:
                # Parse the message
                try:
                    data = json.loads(message)
                    command = data.get('command', '')
                except json.JSONDecodeError:
                    # If not JSON, treat as plain command
                    command = message.strip()
                    
                # Process the command
                if command:
                    logger.debug(f"Processing command from client {client_id}: {command}")
                    response = mud_integration.process_command(client_id, command)
                    
                    # Log the response for debugging
                    if response:
                        trimmed_response = response[:50] + "..." if len(response) > 50 else response
                        logger.debug(f"Command response: {trimmed_response}")
                    
                    # Send response back to client
                    await websocket.send(json.dumps({
                        "type": "response",
                        "message": response
                    }))
                else:
                    logger.warning(f"Empty command received from client {client_id}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Please enter a command."
                    }))
                    
            except Exception as e:
                logger.error(f"Error processing message from client {client_id}: {e}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Error processing your command: {str(e)}"
                }))
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Connection closed for client {client_id}")
    except Exception as e:
        logger.error(f"Unexpected error for client {client_id}: {e}")
    finally:
        # Clean up client connection
        if client_id in active_clients:
            del active_clients[client_id]
        
        # Publish client disconnected event
        logger.info(f"Client disconnected: {client_id}")
        publish("client_disconnected", client_id=client_id)
        
        # Disconnect from MUDpy
        mudpy_interface.disconnect_client(client_id)
        
        # Announce departure to other clients
        await broadcast_message(
            f"* A crew member has left the station.",
            exclude_client=client_id
        )

async def broadcast_message(message, exclude_client=None):
    """
    Broadcast a message to all connected clients.
    
    Args:
        message: The message to broadcast.
        exclude_client: Client ID to exclude from the broadcast.
    """
    if active_clients:
        tasks = []
        for cid, client in active_clients.items():
            if exclude_client is None or cid != exclude_client:
                try:
                    tasks.append(client.send(json.dumps({
                        "type": "broadcast",
                        "message": message
                    })))
                except Exception as e:
                    logger.error(f"Error sending broadcast to client {cid}: {e}")
        
        if tasks:
            await asyncio.gather(*tasks)

def event_handler_setup():
    """
    Set up event handlers for game events.
    """
    # Set up event handlers for player-related events
    subscribe("player_moved", on_player_moved)
    subscribe("item_taken", on_item_taken)
    subscribe("item_dropped", on_item_dropped)
    subscribe("item_used", on_item_used)
    subscribe("player_said", on_player_said)
    
    logger.info("Event handlers registered")

async def on_player_moved(player_id, from_location, to_location):
    """
    Handle player movement events.
    
    Args:
        player_id: The ID of the player who moved.
        from_location: The ID of the previous location.
        to_location: The ID of the new location.
    """
    # Get player name
    player_name = f"Crew Member {player_id % 1000}"
    
    # Get location names
    from_name = mudpy_interface.get_room_name(from_location) or from_location
    to_name = mudpy_interface.get_room_name(to_location) or to_location
    
    # Send notifications to players in affected rooms
    for cid, client in active_clients.items():
        if cid != player_id:
            try:
                client_location = mudpy_interface.get_player_location(cid)
                
                if client_location == from_location:
                    await client.send(json.dumps({
                        "type": "location", 
                        "message": f"* {player_name} has left to {to_name}."
                    }))
                elif client_location == to_location:
                    await client.send(json.dumps({
                        "type": "location",
                        "message": f"* {player_name} has arrived from {from_name}."
                    }))
            except Exception as e:
                logger.error(f"Error sending movement notification to client {cid}: {e}")

async def on_item_taken(item_id, player_id):
    """
    Handle item taken events.
    
    Args:
        item_id: The ID of the item taken.
        player_id: The ID of the player who took the item.
    """
    # Get player name
    player_name = f"Crew Member {player_id % 1000}"
    
    # Get player location
    player_location = mudpy_interface.get_player_location(player_id)
    
    # Get item name
    item_name = mudpy_interface.get_item_name(item_id) or item_id
    
    # Notify other players in the same location
    for cid, client in active_clients.items():
        if cid != player_id and mudpy_interface.get_player_location(cid) == player_location:
            try:
                await client.send(json.dumps({
                    "type": "location",
                    "message": f"* {player_name} picks up {item_name}."
                }))
            except Exception as e:
                logger.error(f"Error sending item taken notification to client {cid}: {e}")

async def on_item_dropped(item_id, player_id):
    """
    Handle item dropped events.
    
    Args:
        item_id: The ID of the item dropped.
        player_id: The ID of the player who dropped the item.
    """
    # Get player name
    player_name = f"Crew Member {player_id % 1000}"
    
    # Get player location
    player_location = mudpy_interface.get_player_location(player_id)
    
    # Get item name
    item_name = mudpy_interface.get_item_name(item_id) or item_id
    
    # Notify other players in the same location
    for cid, client in active_clients.items():
        if cid != player_id and mudpy_interface.get_player_location(cid) == player_location:
            try:
                await client.send(json.dumps({
                    "type": "location",
                    "message": f"* {player_name} drops {item_name}."
                }))
            except Exception as e:
                logger.error(f"Error sending item dropped notification to client {cid}: {e}")

async def on_item_used(item_id, player_id, item_type):
    """
    Handle item used events.
    
    Args:
        item_id: The ID of the item used.
        player_id: The ID of the player who used the item.
        item_type: The type of the item.
    """
    # Get player name
    player_name = f"Crew Member {player_id % 1000}"
    
    # Get player location
    player_location = mudpy_interface.get_player_location(player_id)
    
    # Get item name
    item_name = mudpy_interface.get_item_name(item_id) or item_id
    
    # Notify other players in the same location
    for cid, client in active_clients.items():
        if cid != player_id and mudpy_interface.get_player_location(cid) == player_location:
            try:
                await client.send(json.dumps({
                    "type": "location",
                    "message": f"* {player_name} uses {item_name}."
                }))
            except Exception as e:
                logger.error(f"Error sending item used notification to client {cid}: {e}")

async def on_player_said(client_id, location, message):
    """
    Handle player chat messages.
    
    Args:
        client_id: The ID of the client who sent the message.
        location: The location ID where the message was sent.
        message: The message content.
    """
    # Get player name
    player_name = f"Crew Member {client_id % 1000}"
    
    # Notify other players in the same location
    for cid, client in active_clients.items():
        if cid != client_id and mudpy_interface.get_player_location(cid) == location:
            try:
                await client.send(json.dumps({
                    "type": "chat",
                    "message": f"{player_name} says: {message}"
                }))
            except Exception as e:
                logger.error(f"Error sending chat notification to client {cid}: {e}")

def signal_handler(sig, frame):
    """
    Handle SIGINT and SIGTERM signals for clean shutdown.
    """
    logger.info("Received shutdown signal, cleaning up...")
    
    # Shutdown MUDpy interface
    if mudpy_interface:
        logger.info("Shutting down MUDpy interface")
        try:
            mudpy_interface.shutdown()
        except AttributeError:
            # No shutdown method, just let it be garbage collected
            pass
    
    sys.exit(0)

async def main():
    """
    Main entry point for the server.
    """
    global mudpy_interface, mud_integration
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create MudpyInterface instance
    mudpy_interface = MudpyInterface()
    
    # Create integration with the new engine architecture
    mud_integration = integration.create_integration(mudpy_interface)
    
    # Set up event handlers
    event_handler_setup()
    
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()
    
    # Start WebSocket server
    host = '0.0.0.0'
    port = 8000
    
    logger.info(f"Starting WebSocket server on {host}:{port}")
    
    async with websockets.serve(handle_client, host, port, ping_interval=30, ping_timeout=10):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")