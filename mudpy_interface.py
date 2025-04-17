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
        
        # Sci-Fi world data
        self.world = {
            'rooms': {
                'start': {
                    'name': 'Space Station Alpha - Central Hub',
                    'description': 'A bustling central hub of the space station. Holographic displays show ship arrivals and departures. The artificial gravity feels slightly lighter than Earth standard.',
                    'exits': {'north': 'corridor', 'east': 'medbay', 'south': 'hangar', 'west': 'marketplace'},
                    'items': ['station_map', 'credit_chip']
                },
                'corridor': {
                    'name': 'Main Corridor - North Section',
                    'description': 'A long, sterile corridor with glowing blue lighting strips. Occasional maintenance droids scuttle past, cleaning the metallic floors.',
                    'exits': {'south': 'start', 'north': 'research', 'west': 'quarters'},
                    'items': ['keycard']
                },
                'research': {
                    'name': 'Research Laboratory',
                    'description': 'A high-tech laboratory filled with strange equipment. Holographic displays show DNA sequences and star charts. A containment field in the center holds a pulsing alien artifact.',
                    'exits': {'south': 'corridor'},
                    'items': ['datapad', 'sample_container'],
                    'requires': {'keycard': 'This area requires authorized access. You need a keycard.'}
                },
                'quarters': {
                    'name': 'Crew Quarters',
                    'description': 'A section of small personal quarters for station staff. Your assigned room is here, with a small viewport showing the stars outside.',
                    'exits': {'east': 'corridor'},
                    'items': ['med_kit', 'personal_log']
                },
                'medbay': {
                    'name': 'Medical Bay',
                    'description': 'A sterile medical facility with advanced diagnostic equipment. Several medical droids stand ready to assist patients.',
                    'exits': {'west': 'start', 'north': 'quarantine'},
                    'items': ['medi_spray']
                },
                'quarantine': {
                    'name': 'Quarantine Zone',
                    'description': 'A sealed quarantine area. Warning lights flash red, and the air smells strongly of antiseptic. Something dangerous was contained here.',
                    'exits': {'south': 'medbay'},
                    'items': ['hazmat_suit'],
                    'requires': {'hazmat_suit': 'WARNING: Hazardous environment detected. Entering without protection would be fatal.'}
                },
                'hangar': {
                    'name': 'Docking Hangar',
                    'description': 'A massive hangar where ships dock. Through the atmospheric containment field, you can see the vast expanse of space. Several vessels of different designs are currently docked.',
                    'exits': {'north': 'start', 'east': 'security', 'west': 'maintenance'},
                    'items': ['toolbox']
                },
                'security': {
                    'name': 'Security Checkpoint',
                    'description': 'A security checkpoint with weapon scanners and armored guards. Monitors display surveillance feeds from around the station.',
                    'exits': {'west': 'hangar', 'south': 'detention'},
                    'items': ['stun_baton'],
                    'requires': {'security_clearance': 'The guard stops you: "Only security personnel beyond this point."'}
                },
                'detention': {
                    'name': 'Detention Block',
                    'description': 'A high-security area with reinforced cells. Most are empty, but one contains a strange alien being that watches you with multiple eyes.',
                    'exits': {'north': 'security'},
                    'items': ['strange_crystal']
                },
                'maintenance': {
                    'name': 'Maintenance Tunnels',
                    'description': 'Narrow maintenance tunnels with exposed piping and wiring. The air is warmer here, and you can hear the hum of the station\'s engines.',
                    'exits': {'east': 'hangar', 'west': 'reactor'},
                    'items': ['repair_kit']
                },
                'reactor': {
                    'name': 'Reactor Core',
                    'description': 'The heart of the station - a massive fusion reactor. The intense blue glow and heat make this area uncomfortable. Warning signs are everywhere.',
                    'exits': {'east': 'maintenance'},
                    'items': ['radiation_badge'],
                    'requires': {'radiation_badge': 'DANGER: Lethal radiation levels detected. Proper protection required.'}
                },
                'marketplace': {
                    'name': 'Trading Marketplace',
                    'description': 'A vibrant marketplace where merchants from across the galaxy sell exotic goods. The air is filled with unfamiliar scents and the chatter of various languages.',
                    'exits': {'east': 'start', 'south': 'cantina'},
                    'items': ['alien_fruit', 'star_map']
                },
                'cantina': {
                    'name': 'Nova Cantina',
                    'description': 'A dimly lit cantina where station visitors relax. Strange music plays from speakers, and various species enjoy colorful drinks. A shady-looking dealer sits in the corner.',
                    'exits': {'north': 'marketplace'},
                    'items': ['strange_drink']
                }
            },
            'items': {
                'comms_device': {
                    'name': 'Communications Device',
                    'description': 'A standard-issue communications device that allows you to contact the command center.',
                    'usable': True,
                    'use_effect': 'You contact the command center. "This is Command. We read you. Continue your investigation and report when you have more information."'
                },
                'biometric_scanner': {
                    'name': 'Biometric Scanner',
                    'description': 'A handheld device that can scan for life forms and analyze environmental conditions.',
                    'usable': True,
                    'use_effect': 'You activate your biometric scanner, analyzing the surrounding environment.'
                },
                'keycard': {
                    'name': 'Access Keycard',
                    'description': 'A standard station keycard with security clearance for research areas.',
                    'usable': True,
                    'use_effect': 'You swipe the keycard. The light turns green, indicating successful authentication.'
                },
                'datapad': {
                    'name': 'Research Datapad',
                    'description': 'A datapad containing research notes about an anomaly discovered on a nearby planet.',
                    'usable': True,
                    'use_effect': 'The datapad displays research notes: "The crystalline structure appears to respond to thought patterns. Caution advised - psychological side effects reported by research team."'
                },
                'station_map': {
                    'name': 'Station Holographic Map',
                    'description': 'A small device that projects a 3D map of the station when activated.',
                    'usable': True,
                    'use_effect': 'The device projects a holographic map of Space Station Alpha, highlighting your current position and key areas.'
                },
                'credit_chip': {
                    'name': 'Credit Chip',
                    'description': 'A digital currency chip containing 100 credits, standard currency in this sector.',
                    'usable': True,
                    'use_effect': 'You check your credit balance: 100 credits available.'
                },
                'med_kit': {
                    'name': 'Emergency Medical Kit',
                    'description': 'A compact kit containing medical supplies for treating minor injuries.'
                },
                'medi_spray': {
                    'name': 'Medi-Spray',
                    'description': 'A spray canister of advanced healing nanites that quickly treat wounds.'
                },
                'hazmat_suit': {
                    'name': 'Hazmat Suit',
                    'description': 'A full-body suit that protects against radiation, toxic environments, and certain pathogens.'
                },
                'toolbox': {
                    'name': 'Maintenance Toolbox',
                    'description': 'A standard toolbox containing tools for repairing station systems.'
                },
                'repair_kit': {
                    'name': 'Nano-Repair Kit',
                    'description': 'An advanced repair system that uses nanobots to fix mechanical and electronic systems.'
                },
                'sample_container': {
                    'name': 'Alien Sample Container',
                    'description': 'A sealed container holding tissue samples from an unknown alien species.'
                },
                'radiation_badge': {
                    'name': 'Radiation Protection Badge',
                    'description': 'A badge that, when activated, generates a protective field against radiation.'
                },
                'stun_baton': {
                    'name': 'Security Stun Baton',
                    'description': 'A standard-issue security baton that can deliver an incapacitating electrical charge.'
                },
                'strange_crystal': {
                    'name': 'Strange Pulsing Crystal',
                    'description': 'A crystal that pulses with an inner light. It seems to respond to your thoughts.'
                },
                'personal_log': {
                    'name': 'Personal Log',
                    'description': 'Your personal log recording your mission objectives and observations.'
                },
                'star_map': {
                    'name': 'Interstellar Navigation Chart',
                    'description': 'A detailed chart showing nearby star systems and established jump routes.'
                },
                'alien_fruit': {
                    'name': 'Glowing Alien Fruit',
                    'description': 'A strange fruit that glows with a soft blue light. Supposedly edible for humans.'
                },
                'strange_drink': {
                    'name': 'Nebula Fizz',
                    'description': 'A popular drink that swirls with colors like a nebula. Known for its unusual psychedelic effects.'
                },
                'security_clearance': {
                    'name': 'Security Clearance Badge',
                    'description': 'A badge identifying you as station security personnel, granting access to restricted areas.'
                }
            }
        }
        
        # Player state
        self.player_locations = {}
        self.player_inventories = {}
        self.player_stats = {}
        
        # Help text
        self.help_text = """
Available commands:
- look: Look around your current location
- examine <item>: Look more closely at an item
- go <direction>: Move in a direction (north, south, east, west)
- say <message>: Say something to others in the same room
- inventory (or i): Show your inventory
- take <item>: Pick up an item
- drop <item>: Drop an item
- use <item>: Use an item
- scan: Use your biometric scanner to analyze the environment
- stats: View your current status and statistics
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
            
            # Initialize player inventory
            self.player_inventories[client_id] = ['comms_device', 'biometric_scanner']
            
            # Initialize player stats
            self.player_stats[client_id] = {
                'health': 100,
                'energy': 100,
                'credits': 50,
                'radiation': 0,
                'oxygen': 100
            }
            
            # Send welcome message
            welcome_message = f"""
Welcome to Space Station Alpha!
You are {self.client_sessions[client_id]['character']}, a technician assigned to investigate recent strange occurrences on the station.

Mission Briefing: Multiple systems have been malfunctioning, and there are reports of unusual energy signatures in the research lab. Command suspects sabotage or an unknown technological anomaly.

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
        
        elif command == 'inventory' or command == 'i':
            return self._inventory(client_id)
        
        elif command.startswith('take '):
            item_name = command[5:].strip()
            return self._take(client_id, item_name)
        
        elif command.startswith('drop '):
            item_name = command[5:].strip()
            return self._drop(client_id, item_name)
        
        elif command.startswith('use '):
            item_name = command[4:].strip()
            return self._use(client_id, item_name)
        
        elif command.startswith('examine '):
            item_name = command[8:].strip()
            return self._examine(client_id, item_name)
        
        elif command == 'scan':
            return self._scan(client_id)
        
        elif command == 'stats':
            return self._stats(client_id)
        
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
        
        # Get the new room
        new_room_id = room['exits'][direction]
        new_room = self.world['rooms'].get(new_room_id)
        
        if not new_room:
            return f"Error: The room '{new_room_id}' doesn't exist."
        
        # Check if access requires an item
        if 'requires' in new_room:
            inventory = self.player_inventories.get(client_id, [])
            for required_item, message in new_room['requires'].items():
                if required_item not in inventory:
                    return message
        
        # Move to the new room
        self.player_locations[client_id] = new_room_id
        
        # Update player stats if needed (e.g., radiation in the reactor)
        if client_id in self.player_stats:
            stats = self.player_stats[client_id]
            
            # Reset temporary effects
            stats['radiation'] = 0
            
            # Apply room effects
            if new_room_id == 'reactor' and 'radiation_badge' not in self.player_inventories.get(client_id, []):
                stats['radiation'] = 75
                stats['health'] -= 25
                if stats['health'] < 0:
                    stats['health'] = 0
            
            if new_room_id == 'quarantine' and 'hazmat_suit' not in self.player_inventories.get(client_id, []):
                stats['health'] = 0
        
        # Describe the new room with items
        room_description = f"""
You go {direction}.

{new_room['name']}
{new_room['description']}

Exits: {', '.join(new_room['exits'].keys())}
"""
        
        # Add items if present
        if 'items' in new_room and new_room['items']:
            room_description += "\nYou see:\n"
            for item_id in new_room['items']:
                item = self.world['items'].get(item_id)
                if item:
                    room_description += f"- {item['name']}\n"
                else:
                    room_description += f"- {item_id}\n"
        
        # Add warnings based on room or player stats
        if client_id in self.player_stats:
            stats = self.player_stats[client_id]
            
            if stats['radiation'] > 50:
                room_description += "\nWARNING: Dangerous radiation levels detected! Seek protection immediately.\n"
            
            if stats['health'] <= 0:
                room_description += "\nCRITICAL: You have collapsed due to injuries or environmental hazards. Medical attention required.\n"
                
                # Reset player health and return to the starting point
                stats['health'] = 10
                self.player_locations[client_id] = 'start'
                
                return f"""
You have been critically injured and lost consciousness.

Medical emergency protocols activated. You have been transported to the station's medical bay and stabilized.

{self.world['rooms']['start']['name']}
{self.world['rooms']['start']['description']}

Exits: {', '.join(self.world['rooms']['start']['exits'].keys())}
"""
        
        return room_description
    
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
    
    def _inventory(self, client_id):
        """
        Handle the 'inventory' command.
        
        Args:
            client_id: Unique identifier for the client.
            
        Returns:
            str: List of items in inventory.
        """
        if client_id not in self.player_inventories:
            self.player_inventories[client_id] = []
            
        inventory = self.player_inventories[client_id]
        
        if not inventory:
            return "Your inventory is empty."
            
        inventory_text = "Inventory:\n"
        for item_id in inventory:
            item = self.world['items'].get(item_id)
            if item:
                inventory_text += f"- {item['name']}: {item['description']}\n"
            else:
                inventory_text += f"- {item_id} (Unknown item)\n"
                
        return inventory_text
    
    def _take(self, client_id, item_name):
        """
        Handle the 'take' command.
        
        Args:
            client_id: Unique identifier for the client.
            item_name: Name of the item to take.
            
        Returns:
            str: Result of the take action.
        """
        if client_id not in self.player_locations:
            return "Error: Your location is unknown."
            
        room_id = self.player_locations[client_id]
        room = self.world['rooms'].get(room_id)
        
        if not room:
            return "Error: Invalid room."
            
        # Check if room has items
        if 'items' not in room:
            return f"There's nothing here to take."
            
        # Find the item by partial name match
        item_id = None
        for i in room['items']:
            item = self.world['items'].get(i)
            if item and item_name in i or (item and item_name in item['name'].lower()):
                item_id = i
                break
                
        if not item_id:
            return f"You don't see a '{item_name}' here."
            
        # Initialize inventory if needed
        if client_id not in self.player_inventories:
            self.player_inventories[client_id] = []
            
        # Add to inventory and remove from room
        self.player_inventories[client_id].append(item_id)
        room['items'].remove(item_id)
        
        item = self.world['items'].get(item_id)
        return f"You take the {item['name']}."
    
    def _drop(self, client_id, item_name):
        """
        Handle the 'drop' command.
        
        Args:
            client_id: Unique identifier for the client.
            item_name: Name of the item to drop.
            
        Returns:
            str: Result of the drop action.
        """
        if client_id not in self.player_locations or client_id not in self.player_inventories:
            return "Error: Your location or inventory is unknown."
            
        inventory = self.player_inventories[client_id]
        if not inventory:
            return "You have nothing to drop."
            
        # Find the item by partial name match
        item_id = None
        for i in inventory:
            item = self.world['items'].get(i)
            if item and item_name in i or (item and item_name in item['name'].lower()):
                item_id = i
                break
                
        if not item_id:
            return f"You don't have a '{item_name}'."
            
        # Remove from inventory
        inventory.remove(item_id)
        
        # Add to room
        room_id = self.player_locations[client_id]
        room = self.world['rooms'].get(room_id)
        
        if 'items' not in room:
            room['items'] = []
            
        room['items'].append(item_id)
        
        item = self.world['items'].get(item_id)
        return f"You drop the {item['name']}."
    
    def _use(self, client_id, item_name):
        """
        Handle the 'use' command.
        
        Args:
            client_id: Unique identifier for the client.
            item_name: Name of the item to use.
            
        Returns:
            str: Result of using the item.
        """
        if client_id not in self.player_inventories:
            return "You have nothing to use."
            
        inventory = self.player_inventories[client_id]
        if not inventory:
            return "You have nothing to use."
            
        # Find the item by partial name match
        item_id = None
        for i in inventory:
            item = self.world['items'].get(i)
            if item and item_name in i or (item and item_name in item['name'].lower()):
                item_id = i
                break
                
        if not item_id:
            return f"You don't have a '{item_name}'."
            
        item = self.world['items'].get(item_id)
        
        # Check if the item is usable
        if 'usable' not in item or not item['usable']:
            return f"You can't figure out how to use the {item['name']}."
            
        # Handle special items
        if item_id == 'keycard' and client_id in self.player_locations:
            room_id = self.player_locations[client_id]
            if room_id == 'corridor' and 'research' in self.world['rooms']['corridor']['exits']:
                return f"{item['use_effect']} The research lab door unlocks."
        
        if item_id == 'hazmat_suit' and client_id in self.player_locations:
            room_id = self.player_locations[client_id]
            if room_id == 'medbay' and 'quarantine' in self.world['rooms']['medbay']['exits']:
                return f"You put on the {item['name']}. You should now be protected in hazardous environments."
                
        if item_id == 'radiation_badge' and client_id in self.player_locations:
            room_id = self.player_locations[client_id]
            if room_id == 'maintenance' and 'reactor' in self.world['rooms']['maintenance']['exits']:
                return f"You activate the {item['name']}. A protective field forms around you, shielding you from radiation."
                
        if item_id == 'medi_spray' and client_id in self.player_stats:
            if self.player_stats[client_id]['health'] < 100:
                self.player_stats[client_id]['health'] = 100
                return f"You use the {item['name']} on yourself. Your wounds heal completely."
            else:
                return f"You're already at full health. No need to use the {item['name']}."
        
        # Generic use
        if 'use_effect' in item:
            return item['use_effect']
        else:
            return f"You use the {item['name']}, but nothing special happens."
    
    def _examine(self, client_id, item_name):
        """
        Handle the 'examine' command.
        
        Args:
            client_id: Unique identifier for the client.
            item_name: Name of the item to examine.
            
        Returns:
            str: Detailed description of the item.
        """
        # Check inventory
        inventory_item = None
        if client_id in self.player_inventories:
            for i in self.player_inventories[client_id]:
                item = self.world['items'].get(i)
                if item and item_name in i or (item and item_name in item['name'].lower()):
                    inventory_item = item
                    break
                    
        # Check room
        room_item = None
        if client_id in self.player_locations:
            room_id = self.player_locations[client_id]
            room = self.world['rooms'].get(room_id)
            if room and 'items' in room:
                for i in room['items']:
                    item = self.world['items'].get(i)
                    if item and item_name in i or (item and item_name in item['name'].lower()):
                        room_item = item
                        break
        
        # Report findings
        if inventory_item:
            return f"{inventory_item['name']}: {inventory_item['description']}"
        elif room_item:
            return f"{room_item['name']}: {room_item['description']}"
        else:
            return f"You don't see a '{item_name}' here."
    
    def _scan(self, client_id):
        """
        Handle the 'scan' command.
        
        Args:
            client_id: Unique identifier for the client.
            
        Returns:
            str: Results of the scan.
        """
        # Check if player has a scanner
        if client_id not in self.player_inventories or 'biometric_scanner' not in self.player_inventories[client_id]:
            return "You don't have a biometric scanner."
            
        if client_id not in self.player_locations:
            return "Error: Your location is unknown."
            
        room_id = self.player_locations[client_id]
        room = self.world['rooms'].get(room_id)
        
        if not room:
            return "Error: Invalid room."
            
        # Different scan results based on room
        if room_id == 'research':
            return """SCANNING...
            
Biometric scan complete:
- Unusual energy signature detected
- Non-terrestrial molecular structure present in containment field
- Quantum fluctuations exceeding normal parameters
- WARNING: Psychoactive influence possible - mental shielding recommended"""
        elif room_id == 'quarantine':
            return """SCANNING...
            
Biometric scan complete:
- Pathogen alert: Unknown viral strain detected
- Air quality: Poor (filtered through hazmat suit)
- Radiation levels: Minimal
- Recommendation: Maintain quarantine protocols"""
        elif room_id == 'reactor':
            return """SCANNING...
            
Biometric scan complete:
- Radiation levels: SEVERE (protection active)
- Energy output: 98.7% of maximum
- Structural integrity: 76%
- WARNING: Reactor instability detected - core temperature rising"""
        elif room_id == 'detention':
            return """SCANNING...
            
Biometric scan complete:
- Alien life form detected
- Biological signature: Unknown species
- Telepathic activity measured: High
- Caution advised: Subject appears to be studying you as well"""
        else:
            return """SCANNING...
            
Biometric scan complete:
- Air quality: Normal
- Radiation levels: Minimal
- No unusual energy signatures detected
- Life signs: Only standard human signatures present"""
    
    def _stats(self, client_id):
        """
        Handle the 'stats' command.
        
        Args:
            client_id: Unique identifier for the client.
            
        Returns:
            str: Current player statistics.
        """
        if client_id not in self.player_stats:
            return "Error: Your stats are unknown."
            
        stats = self.player_stats[client_id]
        return f"""Status Report:
- Health: {stats['health']}%
- Energy: {stats['energy']}%
- Credits: {stats['credits']}
- Radiation: {stats['radiation']}%
- Oxygen: {stats['oxygen']}%
"""
    
    def _look(self, client_id):
        """
        Handle the 'look' command - enhanced version.
        
        Args:
            client_id: Unique identifier for the client.
            
        Returns:
            str: Enhanced description of the current location.
        """
        if client_id not in self.player_locations:
            return "Error: Your location is unknown."
        
        room_id = self.player_locations[client_id]
        room = self.world['rooms'].get(room_id)
        
        if not room:
            return "Error: Invalid room."
        
        # Build basic description
        description = f"""
{room['name']}
{room['description']}

Exits: {', '.join(room['exits'].keys())}
"""
        
        # Add items if present
        if 'items' in room and room['items']:
            description += "\nYou see:\n"
            for item_id in room['items']:
                item = self.world['items'].get(item_id)
                if item:
                    description += f"- {item['name']}\n"
                else:
                    description += f"- {item_id}\n"
        
        return description
    
    def shutdown(self):
        """
        Shut down the MUDpy interface.
        """
        logger.info("Shutting down MUDpy interface (demo mode)...")
        
        # Clear client sessions and queues
        self.client_sessions.clear()
        self.response_queues.clear()
        
        logger.info("MUDpy interface shut down.")
