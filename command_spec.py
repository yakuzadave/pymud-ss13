"""
Command specification module for MUDpy SS13.
This module provides classes for defining and matching command patterns.
"""

import re
import logging
from typing import Dict, List, Callable, Optional, Any, Match, Set

# Configure logging
logger = logging.getLogger(__name__)


class CommandSpec:
    """
    Command specification class.

    This class represents a command specification with patterns that can be matched
    against user input.
    """

    def __init__(
        self,
        name: str,
        patterns: List[str],
        help_text: str,
        category: str = "General",
        required_skills: Optional[List[str]] = None,
        terrain_restrictions: Optional[List[str]] = None,
        item_requirements: Optional[List[str]] = None,
        func: Optional[Callable] = None,
    ):
        """
        Initialize a command specification.

        Args:
            name: The name of the command.
            patterns: List of patterns that match this command.
            help_text: Help text for the command.
            category: Command category for grouping in help (default: 'General').
            required_skills: List of skills required to use this command.
            terrain_restrictions: List of terrain types where this command can be used.
            item_requirements: List of items required to use this command.
            func: Function to call when the command is matched.
        """
        self.name = name
        self.patterns = patterns
        self.help_text = help_text
        self.category = category
        self.required_skills = required_skills or []
        self.terrain_restrictions = terrain_restrictions or []
        self.item_requirements = item_requirements or []
        self.func = func
        self.regexes = []

        # Compile patterns into regular expressions
        for pattern in patterns:
            # Convert {param} to named capture groups
            rx = re.escape(pattern)
            # Replace \{param\} with (?P<param>.+)
            rx = re.sub(r"\\\{(\w+)\\\}", r"(?P<\1>.+?)", rx)
            # Compile the regex
            self.regexes.append(re.compile("^" + rx + "$", re.IGNORECASE))

        logger.debug(f"Created command spec '{name}' with {len(patterns)} patterns")

    def match(self, text: str) -> Optional[Dict[str, str]]:
        """
        Match a text against this command's patterns.

        Args:
            text: The text to match.

        Returns:
            Dict of captured parameters, or None if no match.
        """
        for regex in self.regexes:
            match = regex.match(text)
            if match:
                # Return the captured groups as parameters
                params = match.groupdict()
                logger.debug(
                    f"Matched '{text}' to pattern '{regex.pattern}' with params: {params}"
                )
                return params

        return None

    def check_requirements(self, player, location, inventory) -> Optional[str]:
        """
        Check if the command's requirements are met.

        Args:
            player: Player object or data.
            location: Current location data.
            inventory: Player's inventory data.

        Returns:
            None if all requirements are met, or an error message.
        """
        # Check skills
        if self.required_skills:
            player_skills = getattr(player, "skills", set())
            missing_skills = [
                skill for skill in self.required_skills if skill not in player_skills
            ]
            if missing_skills:
                return f"You need the following skills: {', '.join(missing_skills)}"

        # Check terrain
        if self.terrain_restrictions:
            terrain = getattr(location, "terrain", None)
            if terrain not in self.terrain_restrictions:
                return f"This command can only be used in: {', '.join(self.terrain_restrictions)}"

        # Check required items
        if self.item_requirements:
            inventory_ids = {item.id for item in inventory}
            missing_items = [
                item for item in self.item_requirements if item not in inventory_ids
            ]
            if missing_items:
                return f"You need the following items: {', '.join(missing_items)}"

        return None

    def execute(self, **kwargs) -> str:
        """
        Execute the command function with the provided parameters.

        Args:
            **kwargs: Parameters to pass to the function.

        Returns:
            The result of the function call.
        """
        if not self.func:
            return f"Command '{self.name}' is not implemented yet."

        # Extract player, location, and inventory from context
        client_id = kwargs.get("client_id")
        interface = kwargs.get("interface")

        if interface and client_id:
            # Check requirements if we have the necessary context
            player_data = (
                interface.get_player_data(client_id)
                if hasattr(interface, "get_player_data")
                else None
            )
            location = (
                interface.get_player_location(client_id)
                if hasattr(interface, "get_player_location")
                else None
            )
            location_data = (
                interface.get_room_data(location)
                if hasattr(interface, "get_room_data") and location
                else None
            )
            inventory = (
                interface.get_player_inventory(client_id)
                if hasattr(interface, "get_player_inventory")
                else []
            )

            # Check requirements if we have the data
            if player_data and location_data:
                req_error = self.check_requirements(
                    player_data, location_data, inventory
                )
                if req_error:
                    return req_error

        try:
            return self.func(**kwargs)
        except Exception as e:
            logger.error(f"Error executing command '{self.name}': {e}")
            return f"Error executing command: {str(e)}"
