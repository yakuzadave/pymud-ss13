"""Container component for holding items."""

from typing import List, Optional, Dict, Any
import logging
import os
from events import publish
from world import get_world

logger = logging.getLogger(__name__)

class ContainerComponent:
    """Component representing a generic container."""

    def __init__(self, capacity: int = 10, items: Optional[List[str]] = None):
        self.owner = None
        self.capacity = capacity
        self.items: List[str] = items or []

    def _persist(self) -> None:
        """Persist the owning object to disk."""
        if not self.owner:
            return
        world = get_world()
        path = os.path.join(world.data_dir, "world", f"{self.owner.id}.yaml")
        try:
            from persistence import save_game_object
            save_game_object(self.owner, path)
        except Exception as exc:
            logger.error(f"Failed to save container {self.owner.id}: {exc}")

    def add_item(self, item_id: str) -> bool:
        """Add an item to the container, respecting capacity."""
        if len(self.items) >= self.capacity or item_id in self.items:
            return False
        self.items.append(item_id)
        publish("container_item_added", container_id=self.owner.id if self.owner else None, item_id=item_id)
        self._persist()
        return True

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the container."""
        if item_id in self.items:
            self.items.remove(item_id)
            publish("container_item_removed", container_id=self.owner.id if self.owner else None, item_id=item_id)
            self._persist()
            return True
        return False

    def to_dict(self) -> Dict[str, Any]:
        return {"capacity": self.capacity, "items": self.items}
