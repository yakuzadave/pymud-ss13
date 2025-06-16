import logging
from dataclasses import dataclass
from typing import Callable, Optional, Dict, Any

from events import publish
from .antagonists import get_antagonist_system, AntagonistSystem

logger = logging.getLogger(__name__)


@dataclass
class GameMode:
    """Simple definition of a game mode."""

    name: str
    setup: Callable[["RoundManager"], None]
    win_condition: Callable[["RoundManager"], bool]


class RoundManager:
    """Manage round state and win conditions."""

    def __init__(self, antagonist_system: Optional[AntagonistSystem] = None) -> None:
        self.antag_system = antagonist_system or get_antagonist_system()
        self.active: bool = False
        self.mode: Optional[GameMode] = None

    # ------------------------------------------------------------------
    def start_round(self, mode: str) -> None:
        """Start a new round in the specified mode."""
        game_mode = GAME_MODES.get(mode)
        if not game_mode:
            raise ValueError(f"Unknown mode: {mode}")
        self.mode = game_mode
        self.active = True
        logger.info("Starting round in mode: %s", mode)
        publish("round_start", mode=mode)
        game_mode.setup(self)

    # ------------------------------------------------------------------
    def end_round(self) -> Dict[str, Any]:
        """End the current round and report winners."""
        if not self.active or not self.mode:
            return {"winners": []}
        logger.info("Ending round in mode: %s", self.mode.name)
        results = self.antag_system.round_end_check()
        success = self.mode.win_condition(self)
        publish(
            "round_finished",
            mode=self.mode.name,
            winners=results.get("winners"),
            success=success,
        )
        self.active = False
        self.mode = None
        return {"winners": results.get("winners"), "success": success}


def _setup_traitor(manager: RoundManager) -> None:
    # In traitor mode we simply ensure the antagonist system is ready.
    # Antagonists should be assigned externally via admin or join logic.
    publish("mode_traitor_setup")


def _traitor_win(manager: RoundManager) -> bool:
    # Traitors win if any antagonist has completed objectives.
    return any(a.completed for a in manager.antag_system.antagonists.values())


def _setup_cult(manager: RoundManager) -> None:
    publish("mode_cult_setup")


def _cult_win(manager: RoundManager) -> bool:
    # Cult wins if all antagonists complete objectives.
    antags = manager.antag_system.antagonists.values()
    return bool(antags) and all(a.completed for a in antags)


GAME_MODES: Dict[str, GameMode] = {
    "traitor": GameMode("traitor", _setup_traitor, _traitor_win),
    "cult": GameMode("cult", _setup_cult, _cult_win),
}


# Create a global round manager instance
ROUND_MANAGER = RoundManager()


def get_round_manager() -> RoundManager:
    """Return the global round manager instance."""

    return ROUND_MANAGER
