"""
Interface module for MUDpy.
This module provides a simplified mock interface for demo purposes.
For a full integration with the MUDpy server, additional configuration would be needed.
"""

import logging
import queue
import time
import yaml
import os
import sys
from typing import Dict
from persistence import load_aliases, save_aliases

logger = logging.getLogger(__name__)


class MudpyInterface:
    """
    Interface class for MUDpy server (demo version).

    This class simulates communication with a MUD server for demonstration purposes.
    """

    def __init__(
        self, config_file: str = "config.yaml", alias_dir: str = "data/aliases"
    ):
        """
        Initialize the MUDpy interface.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config_file = config_file
        self.config = {}
        self.load_config()

        self.alias_dir = alias_dir
        self.aliases: Dict[str, Dict[str, str]] = {}

        # Client-related data structures
        self.client_sessions = {}
        self.response_queues = {}
        self.player_locations = {}
        self.player_inventories = {}
        self.player_equipment = {}
        self.player_stats = {}

        # World data
        self.world = {
            "rooms": {
                "start": {
                    "name": "Medical Bay",
                    "description": "A sterile room with medical equipment and monitoring devices. Several empty beds line the walls, and a desk with a computer terminal sits in the corner.",
                    "exits": {"north": "corridor", "east": "medbay"},
                },
                "corridor": {
                    "name": "Main Corridor",
                    "description": "A long corridor connecting various parts of the station. The lighting flickers occasionally, creating eerie shadows.",
                    "exits": {
                        "north": "command",
                        "east": "research",
                        "south": "start",
                        "west": "quarters",
                    },
                    "items": ["keycard"],
                },
                "command": {
                    "name": "Command Center",
                    "description": "The nerve center of the station. Multiple screens display status information and external camera feeds. The main viewscreen shows a field of stars.",
                    "exits": {"south": "corridor", "east": "comms"},
                },
                "quarters": {
                    "name": "Crew Quarters",
                    "description": "A living area with several small rooms. Personal effects are scattered around, suggesting a hasty departure.",
                    "exits": {"east": "corridor", "north": "recreation"},
                    "items": ["medi_spray"],
                },
                "recreation": {
                    "name": "Recreation Room",
                    "description": "A lounge area with comfortable seating and entertainment systems. A half-played game of chess sits on a table.",
                    "exits": {"south": "quarters"},
                },
                "medbay": {
                    "name": "Medical Storage",
                    "description": "A room filled with medical supplies and equipment. Cabinets line the walls, and a large refrigeration unit hums in the corner.",
                    "exits": {"west": "start", "north": "quarantine"},
                    "items": ["hazmat_suit"],
                },
                "quarantine": {
                    "name": "Quarantine Zone",
                    "description": "A sealed area used for isolating potentially dangerous biological material. Warning signs indicate extreme caution should be exercised.",
                    "exits": {"south": "medbay"},
                    "requires": {
                        "hazmat_suit": "WARNING: Biohazard detected. Hazmat protection required for entry."
                    },
                },
                "research": {
                    "name": "Research Laboratory",
                    "description": "A high-tech laboratory with advanced scientific equipment. In the center is a containment field housing a pulsing, otherworldly artifact.",
                    "exits": {"west": "corridor", "north": "detention"},
                    "requires": {
                        "keycard": "The door is locked. It requires a keycard for access."
                    },
                },
                "detention": {
                    "name": "Detention Cell",
                    "description": "A secure room with reinforced walls. A force field contains what appears to be a non-human entity. It watches you with apparent intelligence.",
                    "exits": {"south": "research"},
                },
                "comms": {
                    "name": "Communications Center",
                    "description": "A room filled with communication equipment. Long-range transmitters, receivers, and a large subspace antenna control panel.",
                    "exits": {"west": "command", "south": "maintenance"},
                },
                "maintenance": {
                    "name": "Maintenance Access",
                    "description": "A narrow passage with exposed wiring and pipes. Essential systems for the station's operation are accessible from here.",
                    "exits": {"north": "comms", "east": "reactor"},
                    "items": ["radiation_badge"],
                },
                "reactor": {
                    "name": "Reactor Core",
                    "description": "The central power generator for the station. The reactor core pulses with energy, and warning lights indicate higher than normal radiation levels.",
                    "exits": {"west": "maintenance"},
                    "requires": {
                        "radiation_badge": "WARNING: Dangerous radiation levels detected. Radiation protection required for entry."
                    },
                },
            },
            "items": {
                "comms_device": {
                    "name": "Communications Device",
                    "description": "A personal communications device that can receive and transmit messages.",
                    "usable": True,
                    "use_effect": "You activate the communications device, but receive only static.",
                },
                "keycard": {
                    "name": "Security Keycard",
                    "description": "A high-clearance security keycard for accessing restricted areas.",
                    "usable": True,
                    "use_effect": "You swipe the keycard through a reader.",
                },
                "biometric_scanner": {
                    "name": "Biometric Scanner",
                    "description": "A handheld device that can analyze biological signatures and environmental conditions.",
                    "usable": True,
                    "use_effect": "You activate the scanner and analyze your surroundings.",
                },
                "medi_spray": {
                    "name": "Medi-Spray",
                    "description": "A medical spray that can heal minor wounds and injuries.",
                    "usable": True,
                    "use_effect": "You apply the medi-spray to your injuries, feeling instant relief.",
                },
                "hazmat_suit": {
                    "name": "Hazmat Suit",
                    "description": "A protective suit that shields from biological and chemical hazards.",
                    "usable": True,
                    "use_effect": "You put on the hazmat suit, feeling protected from environmental hazards.",
                },
                "radiation_badge": {
                    "name": "Radiation Protection Badge",
                    "description": "A device that creates a protective field against radiation.",
                    "usable": True,
                    "use_effect": "You activate the radiation badge, and a soft glow surrounds you.",
                },
            },
        }

        # Help text shown to players
        self.help_text = """Available commands:
help [command] - Display help information
look [target] - Look at your surroundings or a specific target
go <direction> - Move in a direction (north, south, east, west)
say <message> - Say something to others in the room
inventory, i - List items you are carrying
take <item> - Pick up an item
drop <item> - Drop an item
use <item> - Use an item
examine <item> - Examine an item in detail
scan - Perform environmental scan (requires scanner)
stats - Check your vital statistics
quit - Disconnect from the system
"""

        logger.info("MUDpy interface initialized")

    def load_aliases_for(self, client_id: str) -> None:
        """Load saved aliases for a client into ``self.aliases``."""
        self.aliases[client_id] = load_aliases(
            os.path.join(self.alias_dir, f"{client_id}.yaml")
        )

    def save_aliases_for(self, client_id: str) -> None:
        """Persist aliases for ``client_id`` to disk."""
        if client_id in self.aliases:
            save_aliases(
                self.aliases[client_id],
                os.path.join(self.alias_dir, f"{client_id}.yaml"),
            )

    def load_config(self):
        """
        Load configuration from YAML file.
        If the file doesn't exist, create it with default values.
        """
        try:
            with open(self.config_file, "r") as f:
                self.config = yaml.safe_load(f) or {}
            logger.info(f"Configuration loaded from {self.config_file}")
        except FileNotFoundError:
            self.config = {
                "server": {"host": "0.0.0.0", "port": 8888},
                "world": {"name": "Space Station Alpha", "startup_room": "start"},
            }
            self.save_config()
            logger.info(f"Created default configuration at {self.config_file}")

    def save_config(self):
        """
        Save current configuration to YAML file.
        """
        with open(self.config_file, "w") as f:
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

            # Generate a player name - fixed string formatting
            try:
                # Use modulo as intended for numeric operation
                short_id = (
                    client_id % 1000
                    if isinstance(client_id, int)
                    else hash(str(client_id)) % 1000
                )
                player_name = f"Player_{short_id}"
            except Exception as e:
                # Fallback if anything goes wrong
                player_name = f"Player_{hash(str(client_id)) % 1000}"
                logger.warning(f"Error generating player name: {e}, using fallback")

            # Record client session
            self.client_sessions[client_id] = {
                "authenticated": True,  # Auto-authenticate for demo
                "character": player_name,
                "connected_at": time.time(),
                "location": "start",  # Set location in session too for redundancy
            }

            # Set player location to start room
            self.player_locations[client_id] = "start"
            logger.debug(f"Set player {client_id} location to 'start'")

            # Initialize player inventory
            self.player_inventories[client_id] = ["comms_device", "biometric_scanner"]
            logger.debug(
                f"Initialized inventory for player {client_id}: {self.player_inventories[client_id]}"
            )

            self.player_equipment[client_id] = {}

            # Initialize player stats
            self.player_stats[client_id] = {
                "health": 100,
                "energy": 100,
                "credits": 50,
                "radiation": 0,
                "oxygen": 100,
            }
            logger.debug(
                f"Initialized stats for player {client_id}: {self.player_stats[client_id]}"
            )

            # Load any saved command aliases
            self.load_aliases_for(client_id)

            # Log all client information for debugging
            logger.debug(
                f"Client {client_id} fully initialized: location={self.player_locations.get(client_id)}, "
                f"session={self.client_sessions.get(client_id)}"
            )

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

            # Persist aliases for this client
            self.save_aliases_for(client_id)

            # Remove client session and response queue
            del self.client_sessions[client_id]
            del self.response_queues[client_id]

            if client_id in self.aliases:
                del self.aliases[client_id]

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

        if command == "help":
            return self.help_text

        elif command == "look":
            return self._look(client_id)

        elif command.startswith("go "):
            direction = command[3:].strip()
            return self._go(client_id, direction)

        elif command.startswith("say "):
            message = command[4:].strip()
            return self._say(client_id, message)

        elif command == "inventory" or command == "i":
            return self._inventory(client_id)

        elif command.startswith("take "):
            item_name = command[5:].strip()
            return self._take(client_id, item_name)

        elif command.startswith("drop "):
            item_name = command[5:].strip()
            return self._drop(client_id, item_name)

        elif command.startswith("use "):
            item_name = command[4:].strip()
            return self._use(client_id, item_name)

        elif command.startswith("examine "):
            item_name = command[8:].strip()
            return self._examine(client_id, item_name)

        elif command == "scan":
            return self._scan(client_id)

        elif command == "stats":
            return self._stats(client_id)

        elif command == "quit":
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
        logger.debug(f"_look called for client {client_id}")
        logger.debug(f"Player locations: {self.player_locations}")
        logger.debug(f"Client sessions: {self.client_sessions}")

        # Simplify the client_id handling for this critical method
        # Safety first - if client_id isn't registered, just create a new session
        if client_id not in self.player_locations:
            logger.info(
                f"Client {client_id} not found in player_locations, automatically creating new session"
            )
            self.connect_client(client_id)
            self.player_locations[client_id] = "start"

        room_id = self.player_locations[client_id]
        logger.debug(f"Looking up room with ID: {room_id}")

        room = self.world["rooms"].get(room_id)
        if room:
            logger.debug(f"Found room: {room['name']}")
        else:
            logger.debug("Room not found")

        if not room:
            logger.error(f"Invalid room ID: {room_id}")
            return "Error: Invalid room. Please contact an administrator."

        # Build a detailed response
        response = f"""
{room['name']}
{room['description']}

Exits: {', '.join(room['exits'].keys())}
"""

        # Add items if present
        if "items" in room and room["items"]:
            response += "\nYou see:\n"
            for item_id in room["items"]:
                item = self.world["items"].get(item_id)
                if item:
                    response += f"- {item['name']}\n"
                else:
                    response += f"- {item_id}\n"

        logger.debug(
            f"Generated look response for client {client_id}: {response[:100]}..."
        )
        return response

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
        room = self.world["rooms"].get(room_id)

        if not room:
            return "Error: Invalid room."

        if direction not in room["exits"]:
            return f"You cannot go {direction} from here."

        # Get the new room
        new_room_id = room["exits"][direction]
        new_room = self.world["rooms"].get(new_room_id)

        if not new_room:
            return f"Error: The room '{new_room_id}' doesn't exist."

        # Check if access requires an item
        if "requires" in new_room:
            inventory = self.player_inventories.get(client_id, [])
            for required_item, message in new_room["requires"].items():
                if required_item not in inventory:
                    return message

        # Move to the new room
        self.player_locations[client_id] = new_room_id

        # Update player stats if needed (e.g., radiation in the reactor)
        if client_id in self.player_stats:
            stats = self.player_stats[client_id]

            # Reset temporary effects
            stats["radiation"] = 0

            # Apply room effects
            if (
                new_room_id == "reactor"
                and "radiation_badge" not in self.player_inventories.get(client_id, [])
            ):
                stats["radiation"] = 75
                stats["health"] -= 25
                if stats["health"] < 0:
                    stats["health"] = 0

            if (
                new_room_id == "quarantine"
                and "hazmat_suit" not in self.player_inventories.get(client_id, [])
            ):
                stats["health"] = 0

        # Describe the new room with items
        room_description = f"""
You go {direction}.

{new_room['name']}
{new_room['description']}

Exits: {', '.join(new_room['exits'].keys())}
"""

        # Add items if present
        if "items" in new_room and new_room["items"]:
            room_description += "\nYou see:\n"
            for item_id in new_room["items"]:
                item = self.world["items"].get(item_id)
                if item:
                    room_description += f"- {item['name']}\n"
                else:
                    room_description += f"- {item_id}\n"

        # Add warnings based on room or player stats
        if client_id in self.player_stats:
            stats = self.player_stats[client_id]

            if stats["radiation"] > 50:
                room_description += "\nWARNING: Dangerous radiation levels detected! Seek protection immediately.\n"

            if stats["health"] <= 0:
                room_description += "\nCRITICAL: You have collapsed due to injuries or environmental hazards. Medical attention required.\n"

                # Reset player health and return to the starting point
                stats["health"] = 10
                self.player_locations[client_id] = "start"

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

        # Simple fallback approach - don't try to access client_sessions directly
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

        if not inventory and not self.player_equipment.get(client_id):
            return "Your inventory is empty."

        inventory_text = "Inventory:\n"
        for item_id in inventory:
            item = self.world["items"].get(item_id)
            if item:
                inventory_text += f"- {item['name']}: {item['description']}\n"
            else:
                inventory_text += f"- {item_id} (Unknown item)\n"

        equipped = self.player_equipment.get(client_id, {})
        if equipped:
            inventory_text += "\nEquipped:\n"
            for slot, iid in equipped.items():
                item = self.world["items"].get(iid)
                if item:
                    inventory_text += f"[{slot}] {item['name']}\n"
                else:
                    inventory_text += f"[{slot}] {iid}\n"

        return inventory_text

    def get_inventory_data(self, client_id):
        """Return structured inventory data for UI consumption."""
        if client_id not in self.player_inventories:
            return {"items": [], "equipment": []}

        items = []
        for iid in self.player_inventories.get(client_id, []):
            item = self.world["items"].get(iid, {})
            items.append(
                {
                    "id": iid,
                    "name": item.get("name", iid),
                    "description": item.get("description", ""),
                }
            )

        equipment = []
        for slot, iid in self.player_equipment.get(client_id, {}).items():
            item = self.world["items"].get(iid, {})
            equipment.append({"slot": slot, "id": iid, "name": item.get("name", iid)})

        return {"items": items, "equipment": equipment}

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
        room = self.world["rooms"].get(room_id)

        if not room:
            return "Error: Invalid room."

        # Check if room has items
        if "items" not in room:
            return f"There's nothing here to take."

        # Find the item by partial name match
        item_id = None
        for i in room["items"]:
            item = self.world["items"].get(i)
            if (
                item
                and item_name.lower() in i.lower()
                or (item and item_name.lower() in item["name"].lower())
            ):
                item_id = i
                break

        if not item_id:
            return f"You don't see a '{item_name}' here."

        # Initialize inventory if needed
        if client_id not in self.player_inventories:
            self.player_inventories[client_id] = []

        # Add to inventory and remove from room
        self.player_inventories[client_id].append(item_id)
        room["items"].remove(item_id)

        item = self.world["items"].get(item_id)
        if item:
            return f"You take the {item['name']}."
        else:
            return f"You take the {item_id}."

    def _drop(self, client_id, item_name):
        """
        Handle the 'drop' command.

        Args:
            client_id: Unique identifier for the client.
            item_name: Name of the item to drop.

        Returns:
            str: Result of the drop action.
        """
        if (
            client_id not in self.player_locations
            or client_id not in self.player_inventories
        ):
            return "Error: Your location or inventory is unknown."

        inventory = self.player_inventories[client_id]
        if not inventory:
            return "You have nothing to drop."

        # Find the item by partial name match
        item_id = None
        for i in inventory:
            item = self.world["items"].get(i)
            if (
                item
                and item_name.lower() in i.lower()
                or (item and item_name.lower() in item["name"].lower())
            ):
                item_id = i
                break

        if not item_id:
            return f"You don't have a '{item_name}'."

        # Remove from inventory
        inventory.remove(item_id)

        # Add to room
        room_id = self.player_locations[client_id]
        room = self.world["rooms"].get(room_id)

        if not room:
            # If the room doesn't exist, just remove from inventory
            return f"You drop the {item_id}, but it falls into the void!"

        if "items" not in room:
            room["items"] = []

        room["items"].append(item_id)

        item = self.world["items"].get(item_id)
        if item:
            return f"You drop the {item['name']}."
        else:
            return f"You drop the {item_id}."

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
            item = self.world["items"].get(i)
            if (
                item
                and item_name.lower() in i.lower()
                or (item and item_name.lower() in item["name"].lower())
            ):
                item_id = i
                break

        if not item_id:
            return f"You don't have a '{item_name}'."

        item = self.world["items"].get(item_id)

        # Check if the item exists and is usable
        if not item:
            return f"You can't figure out how to use the {item_id}."

        # Check if the item is usable
        if "usable" not in item or not item["usable"]:
            return f"You can't figure out how to use the {item['name']}."

        # Handle special items
        if item_id == "keycard" and client_id in self.player_locations:
            room_id = self.player_locations[client_id]
            if (
                room_id == "corridor"
                and "research" in self.world["rooms"]["corridor"]["exits"]
            ):
                return f"{item['use_effect']} The research lab door unlocks."

        if item_id == "hazmat_suit" and client_id in self.player_locations:
            room_id = self.player_locations[client_id]
            if (
                room_id == "medbay"
                and "quarantine" in self.world["rooms"]["medbay"]["exits"]
            ):
                return f"You put on the {item['name']}. You should now be protected in hazardous environments."

        if item_id == "radiation_badge" and client_id in self.player_locations:
            room_id = self.player_locations[client_id]
            if (
                room_id == "maintenance"
                and "reactor" in self.world["rooms"]["maintenance"]["exits"]
            ):
                return f"You activate the {item['name']}. A protective field forms around you, shielding you from radiation."

        if item_id == "medi_spray" and client_id in self.player_stats:
            if self.player_stats[client_id]["health"] < 100:
                self.player_stats[client_id]["health"] = 100
                return f"You use the {item['name']} on yourself. Your wounds heal completely."
            else:
                return (
                    f"You're already at full health. No need to use the {item['name']}."
                )

        # Generic use
        if "use_effect" in item:
            return item["use_effect"]
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
                item = self.world["items"].get(i)
                if (
                    item
                    and item_name.lower() in i.lower()
                    or (item and item_name.lower() in item["name"].lower())
                ):
                    inventory_item = item
                    break

        # Check room
        room_item = None
        if client_id in self.player_locations:
            room_id = self.player_locations[client_id]
            room = self.world["rooms"].get(room_id)
            if room and "items" in room:
                for i in room["items"]:
                    item = self.world["items"].get(i)
                    if (
                        item
                        and item_name.lower() in i.lower()
                        or (item and item_name.lower() in item["name"].lower())
                    ):
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
        if (
            client_id not in self.player_inventories
            or "biometric_scanner" not in self.player_inventories[client_id]
        ):
            return "You don't have a biometric scanner."

        if client_id not in self.player_locations:
            return "Error: Your location is unknown."

        room_id = self.player_locations[client_id]
        room = self.world["rooms"].get(room_id)

        if not room:
            return "Error: Invalid room."

        # Different scan results based on room
        if room_id == "research":
            return """SCANNING...

Biometric scan complete:
- Unusual energy signature detected
- Non-terrestrial molecular structure present in containment field
- Quantum fluctuations exceeding normal parameters
- WARNING: Psychoactive influence possible - mental shielding recommended"""
        elif room_id == "quarantine":
            return """SCANNING...

Biometric scan complete:
- Pathogen alert: Unknown viral strain detected
- Air quality: Poor (filtered through hazmat suit)
- Radiation levels: Minimal
- Recommendation: Maintain quarantine protocols"""
        elif room_id == "reactor":
            return """SCANNING...

Biometric scan complete:
- Radiation levels: SEVERE (protection active)
- Energy output: 98.7% of maximum
- Structural integrity: 76%
- WARNING: Reactor instability detected - core temperature rising"""
        elif room_id == "detention":
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
            # Initialize with default values
            self.player_stats[client_id] = {
                "health": 100,
                "energy": 100,
                "credits": 50,
                "radiation": 0,
                "oxygen": 100,
            }

        stats = self.player_stats[client_id]

        status_text = """Status Report:
- Health: {health}%
- Energy: {energy}%
- Credits: {credits}
- Radiation: {radiation}%
- Oxygen: {oxygen}%
""".format(
            **stats
        )

        # Add warnings for concerning status levels
        if stats["health"] < 50:
            status_text += "\nWARNING: Health critical. Seek medical attention.\n"

        if stats["radiation"] > 50:
            status_text += "\nDANGER: High radiation levels detected! Seek radiation protection immediately.\n"

        if stats["oxygen"] < 80:
            status_text += (
                "\nWARNING: Oxygen levels depleting. Verify atmospheric containment.\n"
            )

        return status_text

    def get_player_stats(self, client_id):
        """Return the player's stats if known.

        Args:
            client_id: ID of the player.

        Returns:
            dict | None: Stats dictionary or ``None`` if the player
            has not been initialized.
        """
        return self.player_stats.get(client_id)

    def get_room_name(self, room_id):
        """
        Get the name of a room.

        Args:
            room_id: The ID of the room.

        Returns:
            str: The name of the room, or None if not found.
        """
        if room_id in self.world["rooms"]:
            return self.world["rooms"][room_id].get("name")
        return None

    def get_item_name(self, item_id):
        """
        Get the name of an item.

        Args:
            item_id: The ID of the item.

        Returns:
            str: The name of the item, or None if not found.
        """
        if item_id in self.world["items"]:
            return self.world["items"][item_id].get("name")
        return None

    def get_exits_from_room(self, room_id):
        """Return exits dictionary for a room."""
        room = self.world["rooms"].get(room_id)
        if room:
            return room.get("exits", {})
        return {}

    def get_player_location(self, client_id):
        """
        Get the location of a player.

        Args:
            client_id: The ID of the client/player.

        Returns:
            str: The ID of the player's location, or None if not found.
        """
        return self.player_locations.get(client_id)

    def set_player_location(self, client_id, location):
        """Update a player's location."""
        self.player_locations[client_id] = location

    def shutdown(self):
        """
        Shut down the MUDpy interface.
        """
        logger.info("Shutting down MUDpy interface")

        # Clean up any resources
        # Save current world state if needed
        self.save_config()
