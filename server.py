"""
FastAPI server for MUDpy SS13.
This module provides the main FastAPI application for the MUD.
"""

import asyncio
import json
import logging
import os
import sys
import signal
from typing import Dict, Any, Optional, List
import yaml

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from settings import settings
from connection import ConnectionManager
from mudpy_interface import MudpyInterface
import integration
import engine
from events import publish, subscribe

# Module logger
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MUDpy SS13",
    description="A Space Station 13 inspired MUD engine",
    version="0.1.0",
)

# Create connection manager
connection_manager = ConnectionManager()

# Create MudpyInterface
mudpy_interface = MudpyInterface(settings.config_file)

# Create integration with engine
mud_integration = None

# Client location tracking
client_locations: Dict[str, str] = {}

# Mount static files for web client
web_client_dir = settings.web_client_dir
if os.path.exists(web_client_dir):
    app.mount("/static", StaticFiles(directory=web_client_dir), name="static")
else:
    logger.warning(f"Web client directory {web_client_dir} does not exist, creating it")
    os.makedirs(web_client_dir)
    app.mount("/static", StaticFiles(directory=web_client_dir), name="static")

# Event handlers
async def on_player_moved(player_id: str, from_location: str, to_location: str) -> None:
    """
    Handle player movement events.
    
    Args:
        player_id: The ID of the player who moved.
        from_location: The previous location ID.
        to_location: The new location ID.
    """
    # Update client location tracking
    client_locations[player_id] = to_location
    
    # Get player name
    player_name = f"Crew Member {player_id[-4:]}"
    
    # Get location names
    from_name = mudpy_interface.get_room_name(from_location) or from_location
    to_name = mudpy_interface.get_room_name(to_location) or to_location
    
    # Broadcast to players in the previous location
    await connection_manager.broadcast_to_room(
        {
            "type": "location",
            "message": f"* {player_name} has left to {to_name}."
        },
        from_location,
        client_locations,
        exclude_client=player_id
    )
    
    # Broadcast to players in the new location
    await connection_manager.broadcast_to_room(
        {
            "type": "location",
            "message": f"* {player_name} has arrived from {from_name}."
        },
        to_location,
        client_locations,
        exclude_client=player_id
    )

async def on_item_taken(item_id: str, player_id: str) -> None:
    """
    Handle item taken events.
    
    Args:
        item_id: The ID of the item taken.
        player_id: The ID of the player who took the item.
    """
    # Get player location
    player_location = client_locations.get(player_id)
    if not player_location:
        return
    
    # Get player name
    player_name = f"Crew Member {player_id[-4:]}"
    
    # Get item name
    item_name = mudpy_interface.get_item_name(item_id) or item_id
    
    # Broadcast to players in the same location
    await connection_manager.broadcast_to_room(
        {
            "type": "location",
            "message": f"* {player_name} picks up {item_name}."
        },
        player_location,
        client_locations,
        exclude_client=player_id
    )

async def on_item_dropped(item_id: str, player_id: str) -> None:
    """
    Handle item dropped events.
    
    Args:
        item_id: The ID of the item dropped.
        player_id: The ID of the player who dropped the item.
    """
    # Get player location
    player_location = client_locations.get(player_id)
    if not player_location:
        return
    
    # Get player name
    player_name = f"Crew Member {player_id[-4:]}"
    
    # Get item name
    item_name = mudpy_interface.get_item_name(item_id) or item_id
    
    # Broadcast to players in the same location
    await connection_manager.broadcast_to_room(
        {
            "type": "location",
            "message": f"* {player_name} drops {item_name}."
        },
        player_location,
        client_locations,
        exclude_client=player_id
    )

async def on_item_used(item_id: str, player_id: str, item_type: str) -> None:
    """
    Handle item used events.
    
    Args:
        item_id: The ID of the item used.
        player_id: The ID of the player who used the item.
        item_type: The type of the item.
    """
    # Get player location
    player_location = client_locations.get(player_id)
    if not player_location:
        return
    
    # Get player name
    player_name = f"Crew Member {player_id[-4:]}"
    
    # Get item name
    item_name = mudpy_interface.get_item_name(item_id) or item_id
    
    # Broadcast to players in the same location
    await connection_manager.broadcast_to_room(
        {
            "type": "location",
            "message": f"* {player_name} uses {item_name}."
        },
        player_location,
        client_locations,
        exclude_client=player_id
    )

async def on_player_said(client_id: str, location: str, message: str) -> None:
    """
    Handle player chat messages.
    
    Args:
        client_id: The ID of the player who said something.
        location: The location ID where the message was said.
        message: The message content.
    """
    # Get player name
    player_name = f"Crew Member {client_id[-4:]}"
    
    # Broadcast to players in the same location
    await connection_manager.broadcast_to_room(
        {
            "type": "chat",
            "message": f"{player_name} says: {message}"
        },
        location,
        client_locations,
        exclude_client=client_id
    )

# FastAPI event handlers
@app.on_event("startup")
async def startup_event():
    """Handle application startup."""
    global mud_integration
    
    logger.info("Starting MUDpy SS13 server")
    
    # Create integration with engine
    mud_integration = integration.create_integration(mudpy_interface)
    
    # Register event handlers
    subscribe("player_moved", on_player_moved)
    subscribe("item_taken", on_item_taken)
    subscribe("item_dropped", on_item_dropped)
    subscribe("item_used", on_item_used)
    subscribe("player_said", on_player_said)
    
    logger.info("Event handlers registered")

@app.on_event("shutdown")
async def shutdown_event():
    """Handle application shutdown."""
    logger.info("Shutting down MUDpy SS13 server")
    
    # Shut down MUDpy interface
    if mudpy_interface:
        try:
            mudpy_interface.shutdown()
        except Exception as e:
            logger.error(f"Error shutting down MUDpy interface: {e}")

# API routes
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """Serve the index page."""
    index_path = os.path.join(web_client_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return HTMLResponse("<html><body><h1>MUDpy SS13</h1><p>Welcome to the MUDpy SS13 server!</p></body></html>")

@app.get("/{path:path}")
async def get_static(path: str):
    """Serve static files."""
    full_path = os.path.join(web_client_dir, path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(full_path)
    else:
        # Try index.html as fallback for SPA routing
        index_path = os.path.join(web_client_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            raise HTTPException(status_code=404, detail="File not found")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Handle WebSocket connections.
    
    This endpoint accepts WebSocket connections from clients, processes
    messages, and sends responses.
    """
    # Accept the connection and get client ID
    client_id = await connection_manager.connect(websocket)
    
    try:
        # Send welcome message
        await connection_manager.send_personal_message(
            {
                "type": "system",
                "message": "Welcome to Space Station Alpha - a sci-fi adventure powered by MUDpy SS13!"
            },
            websocket
        )
        
        # Connect client to MUDpy interface
        logger.info(f"Connecting client to MUDpy interface: {client_id}")
        mudpy_interface.connect_client(client_id)
        
        # Publish client connected event
        logger.info(f"Publishing client_connected event for: {client_id}")
        publish("client_connected", client_id=client_id)
        
        # Send initial 'look' command
        try:
            # Send initial 'look' command to get room description
            logger.info(f"Sending initial 'look' command for client: {client_id}")
            initial_response = mud_integration.process_command(client_id, "look")
            
            # Get player location
            player_location = mudpy_interface.get_player_location(client_id)
            if player_location:
                client_locations[client_id] = player_location
            
            # Send response back to client
            await connection_manager.send_personal_message(
                {
                    "type": "response",
                    "message": initial_response if initial_response else "Welcome! You find yourself in a mysterious location."
                },
                websocket
            )
        except Exception as e:
            logger.error(f"Error processing initial look command: {e}")
            await connection_manager.send_personal_message(
                {
                    "type": "error",
                    "message": "Error initializing game state. Please refresh and try again."
                },
                websocket
            )
        
        # Announce new player to other clients
        await connection_manager.broadcast(
            {
                "type": "broadcast",
                "message": f"* A new crew member has boarded the station."
            },
            exclude=websocket
        )
        
        # Wait for messages from the client
        while True:
            # Receive message
            message = await websocket.receive_text()
            
            try:
                # Parse message
                try:
                    data = json.loads(message)
                    command = data.get('command', '')
                except json.JSONDecodeError:
                    # If not JSON, treat as plain command
                    command = message.strip()
                
                # Process command
                if command:
                    logger.debug(f"Processing command from client {client_id}: {command}")
                    response = mud_integration.process_command(client_id, command)
                    
                    # Update player location
                    player_location = mudpy_interface.get_player_location(client_id)
                    if player_location:
                        client_locations[client_id] = player_location
                    
                    # Send response back to client
                    await connection_manager.send_personal_message(
                        {
                            "type": "response",
                            "message": response
                        },
                        websocket
                    )
                else:
                    logger.warning(f"Empty command received from client {client_id}")
                    await connection_manager.send_personal_message(
                        {
                            "type": "error",
                            "message": "Please enter a command."
                        },
                        websocket
                    )
            except Exception as e:
                logger.error(f"Error processing message from client {client_id}: {e}")
                await connection_manager.send_personal_message(
                    {
                        "type": "error",
                        "message": f"Error processing your command: {str(e)}"
                    },
                    websocket
                )
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {client_id}")
    except Exception as e:
        logger.error(f"Unexpected error for client {client_id}: {e}")
    finally:
        # Disconnect from connection manager
        connection_manager.disconnect(websocket)
        
        # Clean up client location tracking
        if client_id in client_locations:
            del client_locations[client_id]
        
        # Publish client disconnected event
        logger.info(f"Publishing client_disconnected event for: {client_id}")
        publish("client_disconnected", client_id=client_id)
        
        # Disconnect from MUDpy interface
        logger.info(f"Disconnecting client from MUDpy interface: {client_id}")
        mudpy_interface.disconnect_client(client_id)
        
        # Announce departure to other clients
        await connection_manager.broadcast(
            {
                "type": "broadcast",
                "message": f"* A crew member has left the station."
            }
        )

# Main entry point
def run_server():
    """Run the server."""
    uvicorn.run(
        "server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )

if __name__ == "__main__":
    run_server()