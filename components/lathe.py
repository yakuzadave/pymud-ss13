from typing import Dict, List, Optional
from events import publish

class LatheComponent:
    """Simple fabrication machine that turns materials into items."""

    def __init__(self, recipes: Optional[Dict[str, List[str]]] = None) -> None:
        self.owner = None
        self.recipes = recipes or {}

    def craft(self, item_id: str, materials: List[str]) -> bool:
        required = self.recipes.get(item_id)
        if not required:
            return False
        if sorted(required) != sorted(materials):
            return False
        publish("lathe_crafted", machine_id=self.owner.id if self.owner else None, item=item_id)
        return True
