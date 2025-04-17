#!/usr/bin/env python3
"""
Interface module for MUDpy.
This module provides a simplified mock interface for demo purposes.
For a full integration with the MUDpy server, additional configuration would be needed.
"""

import logging
import yaml
import os
import threading
import time
import queue
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mudpy_interface')

class MudpyInterface:
    """
    Interface class for MUDpy server (demo version).
    
    This class simulates communication with a MUD server for demonstration purposes.
    """
    
    def __init__(self, config_file='config.yaml'):
        """
        Initialize the MUDpy interface.
        
        Args:
            config_file (str): Path to the configuration file.
        """
        self.config_file = config_file
        self.load_config()
        
        # Dictionary to store client sessions
        self.client_sessions = {}
        
        # Queue for responses from MUDpy
        self.response_queues = {}
        
        # Demo world data
        self.world = {
            'rooms': {
                'start': {
                    'name': 'Town Square',
                    'description': 'You are in the town square. The sun is shining, and people are going about their business.',
                    'exits': {'north': 'forest', 'east': 'shop', 'south': 'inn', 'west': 'blacksmith'}
                },
                'forest': {
                    'name': 'Forest Path',
                    'description': 'You are on a path through a dense forest. Birds chirp overhead, and sunlight filters through the leaves.',
                    'exits': {'south': 'start', 'north': 'clearing'}
                },
                'clearing': {
                    'name': 'Forest Clearing',
                    'description': 'A peaceful clearing in the forest. Wildflowers grow here, and you can see the sky clearly.',
                    'exits': {'south': 'forest'}
                },
                'shop': {
                    'name': 'General Store',
                    'description': 'A small shop with various goods for sale. The shopkeeper nods at you as you enter.',
                    'exits': {'west': 'start'}
                },
                'inn': {
                    'name': 'Cozy Inn',
                    'description': 'A warm and inviting inn. The smell of fresh bread and ale fills the air.',
                    'exits': {'north': 'start'}
                },
                'blacksmith': {
                    'name': 'Blacksmith\'s Forge',
                    'description': 'The heat from the forge is intense. The sound of hammering metal rings through the air.',
                    'exits': {'east': 'start'}
                }
            }
        }
        
        # Current location for players
        self.player_locations = {}
        
        # Help text
        self.help_text = """
Available commands:
- look: Look around your current location
- go <direction>: Move in a direction (north, south, east, west)
- say <message>: Say something to others in the same room
- help: Display this help message
- quit: Log out of the game
"""
        
        # Start the server
        logger.info("MUDpy interface started (demo mode)")
    
    def load_config(self):
        """
        Load configuration from YAML file.
        If the file doesn't exist, create it with default values.
        """
        try:
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)
            
            if self.config is None:
                self.config = {}
        
        except FileNotFoundError:
            # Create default configuration
            self.config = {
                'mudpy_server': {
                    'host': 'localhost',
                    'port': 4000,
                    'timeout': 5
                },
                'websocket_server': {
                    'host': '0.0.0.0',
                    'port': 8000
                },
                'web_client': {
                    'host': '0.0.0.0',
                    'port': 5000
                },
                'storage': {
                    'data_dir': 'data',
                    'save_interval': 300  # 5 minutes
                }
            }
            
            # Save default configuration
            self.save_config()
    
    def save_config(self):
        """
        Save current configuration to YAML file.
        """
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def connect_client(self, client_id):
        """
        Create a new session for a client.
        
        Args:
            client_id: Unique identifier for the client.
        """
        if client_id not in self.client_sessions:
            logger.info(f"Creating new session for client {client_id}")
            
            # Create response queue for this client
            self.response_queues[client_id] = queue.Queue()
            
            # Record client session
            self.client_sessions[client_id] = {
                'authenticated': True,  # Auto-authenticate for demo
                'character': f"Player_{client_id % 1000}",
                'connected_at': time.time()
            }
            
            # Set player location to start room
            self.player_locations[client_id] = 'start'
            
            # Send welcome message
            welcome_message = f"""
Welcome to MUDpy Demo!
You are {self.client_sessions[client_id]['character']}.

{self.world['rooms']['start']['name']}
{self.world['rooms']['start']['description']}

Exits: {', '.join(self.world['rooms']['start']['exits'].keys())}

Type 'help' for a list of commands.
"""
            self.response_queues[client_id].put(welcome_message)
    
    def disconnect_client(self, client_id):
        """
        Clean up resources when a client disconnects.
        
        Args:
            client_id: Unique identifier for the client.
        """
        if client_id in self.client_sessions:
            logger.info(f"Cleaning up session for client {client_id}")
            
            # Remove client session and response queue
            del self.client_sessions[client_id]
            del self.response_queues[client_id]
            
            # Remove player location
            if client_id in self.player_locations:
                del self.player_locations[client_id]
    
    def process_command(self, client_id, command):
        """
        Process a command from a client and return the response.
        
        Args:
            client_id: Unique identifier for the client.
            command: The command to process.
            
        Returns:
            str: The response to the command.
        """
        if client_id not in self.client_sessions:
            return "Error: Not connected. Please refresh and try again."
        
        # Process the command
        command = command.strip().lower()
        
        if command == 'help':
            return self.help_text
        
        elif command == 'look':
            return self._look(client_id)
        
        elif command.startswith('go '):
            direction = command[3:].strip()
            return self._go(client_id, direction)
        
        elif command.startswith('say '):
            message = command[4:].strip()
            return self._say(client_id, message)
        
        elif command == 'quit':
            return "Goodbye! Refresh the page to reconnect."
        
        else:
            return f"Unknown command: '{command}'. Type 'help' for a list of commands."
    
    def _look(self, client_id):
        """
        Handle the 'look' command.
        
        Args:
            client_id: Unique identifier for the client.
            
        Returns:
            str: Description of the current location.
        """
        if client_id not in self.player_locations:
            return "Error: Your location is unknown."
        
        room_id = self.player_locations[client_id]
        room = self.world['rooms'].get(room_id)
        
        if not room:
            return "Error: Invalid room."
        
        return f"""
{room['name']}
{room['description']}

Exits: {', '.join(room['exits'].keys())}
"""
    
    def _go(self, client_id, direction):
        """
        Handle the 'go' command.
        
        Args:
            client_id: Unique identifier for the client.
            direction: Direction to move.
            
        Returns:
            str: Result of the movement.
        """
        if client_id not in self.player_locations:
            return "Error: Your location is unknown."
        
        room_id = self.player_locations[client_id]
        room = self.world['rooms'].get(room_id)
        
        if not room:
            return "Error: Invalid room."
        
        if direction not in room['exits']:
            return f"You cannot go {direction} from here."
        
        # Move to the new room
        new_room_id = room['exits'][direction]
        new_room = self.world['rooms'].get(new_room_id)
        
        if not new_room:
            return f"Error: The room '{new_room_id}' doesn't exist."
        
        self.player_locations[client_id] = new_room_id
        
        return f"""
You go {direction}.

{new_room['name']}
{new_room['description']}

Exits: {', '.join(new_room['exits'].keys())}
"""
    
    def _say(self, client_id, message):
        """
        Handle the 'say' command.
        
        Args:
            client_id: Unique identifier for the client.
            message: Message to say.
            
        Returns:
            str: Confirmation of the message.
        """
        if not message:
            return "Say what?"
        
        character_name = self.client_sessions[client_id]['character']
        
        # In a real implementation, this would broadcast to all players in the same room
        return f"You say: {message}"
    
    def _get_response(self, client_id):
        """
        Get the response for a client.
        
        Args:
            client_id: Unique identifier for the client.
            
        Returns:
            str: The response, or an error message if no response is available.
        """
        if client_id not in self.response_queues:
            return "Error: Client not connected."
        
        # Check if there's a response in the queue
        try:
            response = self.response_queues[client_id].get(block=False)
            return response
        except queue.Empty:
            return "No response available."
    
    def shutdown(self):
        """
        Shut down the MUDpy interface.
        """
        logger.info("Shutting down MUDpy interface (demo mode)...")
        
        # Clear client sessions and queues
        self.client_sessions.clear()
        self.response_queues.clear()
        
        logger.info("MUDpy interface shut down.")
