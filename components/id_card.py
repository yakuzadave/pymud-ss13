"""ID card component representing an access badge."""

from typing import Dict, Any


class IDCardComponent:
    """Simple component storing an access level."""

    def __init__(self, access_level: int = 0) -> None:
        self.owner = None
        self.access_level = access_level

    def to_dict(self) -> Dict[str, Any]:
        return {"access_level": self.access_level}
