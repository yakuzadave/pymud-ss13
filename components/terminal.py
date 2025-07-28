from dataclasses import dataclass
from typing import Optional

from events import publish


@dataclass
class TerminalComponent:
    """Computer terminal providing an interface to station subsystems."""

    term_type: str
    location: Optional[str] = None

    def __post_init__(self) -> None:
        self.owner = None

    def on_added(self) -> None:
        from systems.terminal import get_terminal_system

        get_terminal_system().register_terminal(self.owner.id, self)

    def execute(self, command: str, *args: str) -> Optional[str]:
        from systems.terminal import get_terminal_system

        publish(
            "terminal_accessed", terminal_id=self.owner.id, command=command
        )
        return get_terminal_system().execute(self.owner.id, command, *args)
