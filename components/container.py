"""Container component for holding items."""

from typing import List, Optional, Dict, Any
import logging
import os
import threading
from events import publish
from world import get_world

logger = logging.getLogger(__name__)


class ContainerComponent:
    """Component representing a generic, openable container."""

    def __init__(
        self,
        capacity: int = 10,
        items: Optional[List[str]] = None,
        is_open: bool = False,
        is_locked: bool = False,
        access_level: int = 0,
    ):
        self.owner = None
        self.capacity = capacity
        self.items: List[str] = items or []
        self.is_open = is_open
        self.is_locked = is_locked
        self.access_level = access_level
        self._lock = threading.Lock()

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
        with self._lock:
            if len(self.items) >= self.capacity or item_id in self.items:
                return False
            self.items.append(item_id)
        publish(
            "container_item_added",
            container_id=self.owner.id if self.owner else None,
            item_id=item_id,
        )
        self._persist()
        return True

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the container."""
        with self._lock:
            if item_id in self.items:
                self.items.remove(item_id)
            else:
                return False
        publish(
            "container_item_removed",
            container_id=self.owner.id if self.owner else None,
            item_id=item_id,
        )
        self._persist()
        return True

    # ------------------------------------------------------------------
    # Open/Close/Lock mechanics
    # ------------------------------------------------------------------
    def open(self, player_id: str, access_code: int = 0) -> str:
        """Attempt to open the container."""
        if self.is_open:
            return "The container is already open."

        if self.is_locked:
            if access_code >= self.access_level:
                self.is_locked = False
            else:
                return "The container is locked."

        self.is_open = True
        publish(
            "container_opened",
            container_id=self.owner.id if self.owner else None,
            player_id=player_id,
        )
        self._persist()
        return f"You open the {self.owner.name}."

    def close(self, player_id: str) -> str:
        """Attempt to close the container."""
        if not self.is_open:
            return "The container is already closed."

        self.is_open = False
        publish(
            "container_closed",
            container_id=self.owner.id if self.owner else None,
            player_id=player_id,
        )
        self._persist()
        return f"You close the {self.owner.name}."

    def lock(self, player_id: str, access_code: int) -> str:
        if self.is_locked:
            return "The container is already locked."
        if access_code < self.access_level:
            return "You don't have authorization to lock this container."

        self.is_locked = True
        self.is_open = False
        publish(
            "container_locked",
            container_id=self.owner.id if self.owner else None,
            player_id=player_id,
        )
        self._persist()
        return f"You lock the {self.owner.name}."

    def unlock(self, player_id: str, access_code: int) -> str:
        if not self.is_locked:
            return "The container is already unlocked."
        if access_code < self.access_level:
            return "You don't have authorization to unlock this container."

        self.is_locked = False
        publish(
            "container_unlocked",
            container_id=self.owner.id if self.owner else None,
            player_id=player_id,
        )
        self._persist()
        return f"You unlock the {self.owner.name}."

    def hack(self, player_id: str, skill: int = 0) -> str:
        """Attempt to bypass the container lock."""
        if not self.is_locked:
            return "The container is already unlocked."
        if skill < self.access_level:
            return "You fail to hack the container."

        self.is_locked = False
        publish(
            "container_hacked",
            container_id=self.owner.id if self.owner else None,
            player_id=player_id,
        )
        self._persist()
        return f"You hack the {self.owner.name} and unlock it."

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capacity": self.capacity,
            "items": self.items,
            "is_open": self.is_open,
            "is_locked": self.is_locked,
            "access_level": self.access_level,
        }
