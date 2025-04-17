"""
Command specification module for MUDpy SS13.
This module provides classes for defining and matching command patterns.
"""

import re
import logging
from typing import Dict, List, Callable, Optional, Any, Match

# Configure logging
logger = logging.getLogger(__name__)

class CommandSpec:
    """
    Command specification class.
    
    This class represents a command specification with patterns that can be matched
    against user input.
    """
    
    def __init__(self, name: str, patterns: List[str], help_text: str, func: Optional[Callable] = None):
        """
        Initialize a command specification.
        
        Args:
            name: The name of the command.
            patterns: List of patterns that match this command.
            help_text: Help text for the command.
            func: Function to call when the command is matched.
        """
        self.name = name
        self.patterns = patterns
        self.help_text = help_text
        self.func = func
        self.regexes = []
        
        # Compile patterns into regular expressions
        for pattern in patterns:
            # Convert {param} to named capture groups
            rx = re.escape(pattern)
            # Replace \{param\} with (?P<param>\S+)
            rx = re.sub(r"\\\{(\w+)\\\}", r"(?P<\1>.+)", rx)
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
                logger.debug(f"Matched '{text}' to pattern '{regex.pattern}' with params: {params}")
                return params
        
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
        
        try:
            return self.func(**kwargs)
        except Exception as e:
            logger.error(f"Error executing command '{self.name}': {e}")
            return f"Error executing command: {str(e)}"