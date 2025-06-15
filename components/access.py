"""Access control component enforcing security levels."""

from typing import Dict, Any
import logging
from events import publish

logger = logging.getLogger(__name__)


class AccessControlComponent:
    """Component that checks access against a required level."""

    def __init__(self, required_level: int = 0):
        self.owner = None
        self.required_level = required_level

    def check_access(self, level: int) -> bool:
        allowed = level >= self.required_level
        event = "access_granted" if allowed else "access_denied"
        publish(
            event,
            object_id=self.owner.id if self.owner else None,
            required_level=self.required_level,
            access_level=level,
        )
        return allowed

    def to_dict(self) -> Dict[str, Any]:
        return {"required_level": self.required_level}
