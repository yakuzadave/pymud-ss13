"""
NPC component for MUDpy SS13.
Represents a non-player character with a role and optional dialogue.
"""

from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class NPCComponent:
    """Component representing an NPC in the game world."""

    def __init__(self, role: str = "crew", dialogue: Optional[List[str]] = None):
        self.owner = None
        self.role = role
        self.dialogue = dialogue or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert this component to a serializable dict."""
        return {
            "role": self.role,
            "dialogue": self.dialogue,
        }
