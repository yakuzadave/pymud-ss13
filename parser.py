"""
Command parser module for MUDpy SS13.
This module loads command specifications and handles command dispatching.
"""

import os
import yaml
import logging
import difflib
from typing import Dict, List, Optional, Any, Callable

from command_spec import CommandSpec

# Configure logging
logger = logging.getLogger(__name__)

class CommandParser:
    """
    Command parser class.
    
    This class loads command specifications from a YAML file and dispatches
    commands to the appropriate handlers.
    """
    
    def __init__(self, commands_file: str = 'data/commands.yaml'):
        """
        Initialize the command parser.
        
        Args:
            commands_file: Path to the YAML file containing command specifications.
        """
        self.commands_file = commands_file
        self.command_specs = []
        self.command_handlers = {}
        
        logger.info(f"Initializing command parser with {commands_file}")
    
    def register_handler(self, command_name: str, handler: Callable) -> None:
        """
        Register a handler function for a command.
        
        Args:
            command_name: The name of the command.
            handler: The function to handle the command.
        """
        self.command_handlers[command_name] = handler
        logger.debug(f"Registered handler for command '{command_name}'")
    
    def load_commands(self) -> None:
        """Load command specifications from the YAML file."""
        if not os.path.exists(self.commands_file):
            logger.error(f"Commands file not found: {self.commands_file}")
            return
        
        try:
            with open(self.commands_file, 'r') as f:
                commands_data = yaml.safe_load(f)
            
            self.command_specs = []
            for cmd in commands_data:
                name = cmd.get('name', '')
                patterns = cmd.get('patterns', [])
                help_text = cmd.get('help', '')
                category = cmd.get('category', 'General')
                required_skills = cmd.get('required_skills', [])
                terrain_restrictions = cmd.get('terrain_restrictions', [])
                item_requirements = cmd.get('item_requirements', [])
                
                handler = self.command_handlers.get(name)
                
                spec = CommandSpec(
                    name=name, 
                    patterns=patterns, 
                    help_text=help_text,
                    category=category,
                    required_skills=required_skills,
                    terrain_restrictions=terrain_restrictions,
                    item_requirements=item_requirements,
                    func=handler
                )
                self.command_specs.append(spec)
            
            logger.info(f"Loaded {len(self.command_specs)} command specifications")
        except Exception as e:
            logger.error(f"Error loading commands: {e}")
    
    def get_command_names(self) -> List[str]:
        """
        Get a list of all command names.
        
        Returns:
            List of command names.
        """
        return [spec.name for spec in self.command_specs]
    
    def get_categories(self) -> List[str]:
        """
        Get a list of all command categories.
        
        Returns:
            List of command categories.
        """
        categories = set()
        for spec in self.command_specs:
            categories.add(spec.category)
        return sorted(list(categories))
    
    def get_commands_by_category(self) -> Dict[str, List[str]]:
        """
        Get commands grouped by category.
        
        Returns:
            Dict mapping categories to lists of command names.
        """
        result = {}
        for spec in self.command_specs:
            if spec.category not in result:
                result[spec.category] = []
            result[spec.category].append(spec.name)
        
        # Sort commands within each category
        for category in result:
            result[category].sort()
        
        return result
    
    def get_help(self, command_name: Optional[str] = None) -> str:
        """
        Get help text for a command or list all commands.
        
        Args:
            command_name: The name of the command to get help for, or None to list all commands.
            
        Returns:
            Help text for the command or a list of all commands.
        """
        if command_name:
            for spec in self.command_specs:
                if spec.name.lower() == command_name.lower():
                    # Build detailed help for this command
                    help_text = f"Help for '{spec.name}' ({spec.category}):\n"
                    help_text += f"{spec.help_text}\n\n"
                    
                    # Add patterns
                    help_text += "Patterns:\n"
                    for pattern in spec.patterns:
                        help_text += f"  {pattern}\n"
                    
                    # Add requirements if any
                    if spec.required_skills:
                        help_text += f"\nRequired skills: {', '.join(spec.required_skills)}"
                    
                    if spec.terrain_restrictions:
                        help_text += f"\nUsable in: {', '.join(spec.terrain_restrictions)}"
                    
                    if spec.item_requirements:
                        help_text += f"\nRequired items: {', '.join(spec.item_requirements)}"
                    
                    return help_text
            
            # Try to find close matches if exact match not found
            close_matches = difflib.get_close_matches(command_name, self.get_command_names(), n=3)
            if close_matches:
                return f"Unknown command '{command_name}'. Did you mean: {', '.join(close_matches)}?"
            else:
                return f"Unknown command '{command_name}'."
        else:
            # Group commands by category
            commands_by_category = self.get_commands_by_category()
            
            help_text = "Available commands by category:\n"
            
            # List commands by category
            for category in sorted(commands_by_category.keys()):
                help_text += f"\n{category}:\n"
                for cmd in commands_by_category[category]:
                    help_text += f"  {cmd}\n"
            
            help_text += "\nType 'help <command>' for more information on a specific command."
            return help_text
    
    def dispatch(self, text: str, context: Dict[str, Any]) -> str:
        """
        Dispatch a command to the appropriate handler.
        
        Args:
            text: The command text to parse.
            context: Context information for command execution.
            
        Returns:
            The result of the command execution.
        """
        if not text:
            return "Please enter a command. Type 'help' for a list of commands."
        
        # Clean up the input text
        text = text.strip()
        
        # Check for help command first
        if text.lower() == 'help':
            return self.get_help()
        elif text.lower().startswith('help '):
            command_name = text[5:].strip()
            return self.get_help(command_name)
        
        # Try to match the command against all specs
        for spec in self.command_specs:
            params = spec.match(text)
            if params is not None:
                # Command matched
                logger.debug(f"Command '{text}' matched to '{spec.name}'")
                
                # Add context to params
                params.update(context)
                
                # Execute the command
                if spec.func:
                    return spec.execute(**params)
                else:
                    return f"Command '{spec.name}' is not implemented yet."
        
        # No match found, try to suggest similar commands
        first_word = text.split()[0].lower()
        close_matches = difflib.get_close_matches(first_word, self.get_command_names(), n=3)
        
        if close_matches:
            return f"Unknown command '{first_word}'. Did you mean: {', '.join(close_matches)}?"
        else:
            return f"Unknown command. Type 'help' for a list of commands."
