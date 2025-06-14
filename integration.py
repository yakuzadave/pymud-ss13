"""
Integration module for connecting MudpyInterface with the new component-based engine.
This provides backward compatibility while we transition to the new architecture.
"""

import logging
from typing import Dict, Any, Optional
from engine import MudEngine
from world import get_world, GameObject
from components.room import RoomComponent
from components.door import DoorComponent
from components.item import ItemComponent
from components.npc import NPCComponent
from components.player import PlayerComponent
from events import subscribe, publish
import yaml
import os

# Set up module logger
logger = logging.getLogger(__name__)

class MudpyIntegration:
    """
    Integration class that connects the MudpyInterface with the new engine.
    """

    def __init__(self, interface):
        """
        Initialize the integration.

        Args:
            interface: The MudpyInterface instance to integrate with.
        """
        self.interface = interface
        self.engine = MudEngine(interface)
        self.world = get_world()

        # Initialize the world with game data
        self._init_world()

        # Set up event handlers
        self._setup_event_handlers()

        logger.info("MudpyIntegration initialized")

    def _init_world(self):
        """
        Initialize the world with game data from YAML files.
        """
        data_dir = self.world.data_dir

        # Create the data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)

        # Create player-specific and world-specific folders
        os.makedirs(os.path.join(data_dir, "players"), exist_ok=True)
        os.makedirs(os.path.join(data_dir, "world"), exist_ok=True)

        # Load rooms
        if os.path.exists(os.path.join(data_dir, "rooms.yaml")):
            self.world.load_rooms("rooms.yaml")

        # Load items
        if os.path.exists(os.path.join(data_dir, "items.yaml")):
            self.world.load_items("items.yaml")

        # Note: In a real implementation, you'd also load players, NPCs, etc.
        if os.path.exists(os.path.join(data_dir, "npcs.yaml")):
            self.world.load_npcs("npcs.yaml")


        # Load any player files if present
        if os.path.exists(os.path.join(data_dir, "players.yaml")):
            self.world.load_from_file("players.yaml")

        players_dir = os.path.join(data_dir, "players")
        if os.path.isdir(players_dir):
            for fname in os.listdir(players_dir):
                if fname.endswith(".yaml"):
                    self.world.load_from_file(os.path.join("players", fname))

        # Load saved player objects
        from persistence import load_players
        load_players(os.path.join(self.world.data_dir, "players"), self.world)


        logger.info("World initialization complete")


    def _setup_event_handlers(self):
        """
        Set up event handlers for integration.
        """
        # Player movement events
        subscribe("player_moved", self._on_player_moved)

        # Item events
        subscribe("item_taken", self._on_item_taken)
        subscribe("item_dropped", self._on_item_dropped)
        subscribe("item_used", self._on_item_used)

        # Communication events
        subscribe("player_said", self._on_player_said)

        # Connection events
        subscribe("client_connected", self._on_client_connected)
        subscribe("client_disconnected", self._on_client_disconnected)

        logger.info("Event handlers registered")

    def _on_client_connected(self, client_id):
        """
        Handle client connection events.

        Args:
            client_id: The ID of the client.
        """
        # Convert to string if needed for manipulation
        client_id_str = str(client_id)
        logger.debug(f"Client connected event handler, client_id: {client_id} (type: {type(client_id)})")

        # Create a player game object for this client - use string ID for consistency
        player_id = f"player_{client_id_str}"
        player_obj = GameObject(
            id=player_id,
            name=f"Player {client_id_str[-4:]}",  # Use the last 4 digits of the client_id as the player name
            description="A space station crew member.",
            location="start"  # Start in the Central Hub
        )

        # Add player component
        player_comp = PlayerComponent(
            inventory=["comms_device", "biometric_scanner"],
            stats={
                "health": 100.0,
                "energy": 100.0,
                "oxygen": 100.0,
                "radiation": 0.0
            },
            access_level=0,
            current_location="start"
        )
        player_obj.add_component("player", player_comp)

        # Register the player in the world
        self.world.register(player_obj)

        # Ensure client is registered in interface
        if client_id not in self.interface.player_locations:
            logger.debug(f"Adding client {client_id} to player_locations in interface")
            self.interface.player_locations[client_id] = 'start'

        if client_id not in self.interface.client_sessions:
            logger.debug(f"Client {client_id} not found in client_sessions, reconnecting")
            self.interface.connect_client(client_id)

        logger.info(f"Created player game object for client {client_id}")

    def _on_client_disconnected(self, client_id):
        """
        Handle client disconnection events.

        Args:
            client_id: The ID of the client.
        """
        # Find and remove the player game object
        player_id = f"player_{client_id}"
        player_obj = self.world.get_object(player_id)

        if player_obj:
            save_path = os.path.join(self.world.data_dir, "players", f"{player_id}.yaml")
            try:
                from persistence import save_game_object
                save_game_object(player_obj, save_path)
            except Exception as e:
                logger.error(f"Failed to save player {player_id}: {e}")

            if player_id in self.world.objects:
                del self.world.objects[player_id]
                logger.info(f"Removed player game object for client {client_id}")
        else:
            logger.warning(f"Player object not found for client {client_id}")

    def _on_player_moved(self, player_id: str, from_location: str, to_location: str):
        """
        Handle player movement events.

        Args:
            player_id: The ID of the player.
            from_location: The ID of the previous location.
            to_location: The ID of the new location.
        """
        # Update the player's location in the MudpyInterface
        if player_id in self.interface.client_sessions:
            self.interface.client_sessions[player_id]["location"] = to_location
            logger.debug(f"Updated player {player_id} location to {to_location}")

    def _on_item_taken(self, item_id: str, player_id: str):
        """
        Handle item taken events.

        Args:
            item_id: The ID of the item.
            player_id: The ID of the player.
        """
        # Update the player's inventory in the MudpyInterface
        if player_id in self.interface.client_sessions:
            if "inventory" not in self.interface.client_sessions[player_id]:
                self.interface.client_sessions[player_id]["inventory"] = []

            self.interface.client_sessions[player_id]["inventory"].append(item_id)
            logger.debug(f"Added item {item_id} to player {player_id}'s inventory")

    def _on_item_dropped(self, item_id: str, player_id: str):
        """
        Handle item dropped events.

        Args:
            item_id: The ID of the item.
            player_id: The ID of the player.
        """
        # Update the player's inventory in the MudpyInterface
        if player_id in self.interface.client_sessions:
            if "inventory" in self.interface.client_sessions[player_id]:
                if item_id in self.interface.client_sessions[player_id]["inventory"]:
                    self.interface.client_sessions[player_id]["inventory"].remove(item_id)
                    logger.debug(f"Removed item {item_id} from player {player_id}'s inventory")

    def _on_item_used(self, item_id: str, player_id: str, item_type: str):
        """
        Handle item used events.

        Args:
            item_id: The ID of the item.
            player_id: The ID of the player.
            item_type: The type of item.
        """
        # Handle special item effects in the MudpyInterface
        # This is just a placeholder - in a real implementation, you'd have more logic here
        logger.debug(f"Player {player_id} used item {item_id} of type {item_type}")

    def _on_player_said(self, client_id: str, location: str, message: str):
        """
        Handle player communication events.

        Args:
            client_id: The ID of the client.
            location: The location where the message was said.
            message: The message content.
        """
        # Relay the message to other players in the same location
        # This is just a placeholder - in a real implementation, you'd iterate through
        # all players in the same location and send them the message
        logger.debug(f"Player {client_id} said '{message}' in {location}")

    def process_command(self, client_id, command: str) -> str:
        """
        Process a command using the new engine.

        Args:
            client_id: The ID of the client (could be int or str).
            command: The command to process.

        Returns:
            str: The response to the command.
        """
        # Process the command using the engine
        # Convert client_id to string to ensure compatibility
        return self.engine.process_command(str(client_id), command)

# This function will be called to create the integration when needed
def create_integration(interface) -> MudpyIntegration:
    """
    Create an integration between MudpyInterface and the new engine.

    Args:
        interface: The MudpyInterface instance.

    Returns:
        MudpyIntegration: The integration instance.
    """
    return MudpyIntegration(interface)
