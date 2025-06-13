"""Container component for holding items."""

from typing import List, Optional, Dict, Any
import logging
from events import publish

logger = logging.getLogger(__name__)

class ContainerComponent:
    """Component representing a generic container."""

    def __init__(self, capacity: int = 10, items: Optional[List[str]] = None):
        self.owner = None
        self.capacity = capacity
        self.items: List[str] = items or []

    def add_item(self, item_id: str) -> bool:
        """Add an item to the container."""
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item_id)
        publish("container_item_added", container_id=self.owner.id if self.owner else None, item_id=item_id)
        return True

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the container."""
        if item_id in self.items:
            self.items.remove(item_id)
            publish("container_item_removed", container_id=self.owner.id if self.owner else None, item_id=item_id)
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {"capacity": self.capacity, "items": self.items}
