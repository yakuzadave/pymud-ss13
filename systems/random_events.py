"""Random event system for MUDpy SS13."""

import logging
import os
from typing import Dict, Any
import yaml

logger = logging.getLogger(__name__)

class RandomEventSystem:
    """System that manages random station events."""

    def __init__(self, events_file: str = "data/random_events.yaml"):
        self.events_file = events_file
        self.events: Dict[str, Dict[str, Any]] = {}

    def load_events(self) -> None:
        """Load random event definitions from ``self.events_file``."""
        if not os.path.exists(self.events_file):
            logger.warning(
                f"Random events file not found: {self.events_file}"
            )
            self.events = {}
            return

        try:
            with open(self.events_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or []

            if not isinstance(data, list):
                logger.error(
                    "Expected a list of events in %s, got %s",
                    self.events_file,
                    type(data),
                )
                self.events = {}
                return

            self.events = {
                evt.get("id", f"event_{idx}"): evt
                for idx, evt in enumerate(data)
            }
            logger.info(
                "Loaded %d random events from %s",
                len(self.events),
                self.events_file,
            )
        except Exception as e:  # pragma: no cover - simple log on failure
            logger.error("Error loading random events: %s", e)
            self.events = {}
