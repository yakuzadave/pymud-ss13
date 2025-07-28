"""Station computer terminal interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class Terminal:
    terminal_id: str
    term_type: str
    location: Optional[str] = None
    command_log: List[str] = None


class TerminalSystem:
    """Manage terminals and route commands to subsystems."""

    def __init__(self) -> None:
        self.terminals: Dict[str, Terminal] = {}

    # ------------------------------------------------------------------
    def register_terminal(self, terminal_id: str, comp: "TerminalComponent") -> None:
        self.terminals[terminal_id] = Terminal(terminal_id, comp.term_type, comp.location, [])
        publish("terminal_registered", terminal_id=terminal_id, type=comp.term_type)

    # ------------------------------------------------------------------
    def execute(self, terminal_id: str, command: str, *args: str) -> Optional[str]:
        term = self.terminals.get(terminal_id)
        if not term:
            return None
        term.command_log.append(command)
        publish("terminal_command", terminal_id=terminal_id, command=command)

        from commands import consoles

        if term.term_type == "engineering":
            target = args[0] if args else None
            return consoles.engconsole_handler("terminal", action=command, target=target)
        if term.term_type == "cargo":
            return consoles.cargoconsole_handler("terminal", action=command, *args)
        if term.term_type == "security":
            target = args[0] if args else None
            return consoles.secconsole_handler("terminal", action=command, target=target)
        return None


_TERMINAL_SYSTEM = TerminalSystem()


def get_terminal_system() -> TerminalSystem:
    """Return the global terminal system."""

    return _TERMINAL_SYSTEM
