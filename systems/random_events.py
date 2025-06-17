"""Random events system for MUDpy SS13."""

import asyncio
import logging
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path

import yaml
from events import publish

logger = logging.getLogger(__name__)


@dataclass
class RandomEvent:
    """Definition of a random event."""

    id: str
    name: str
    weight: int = 1
    params: Dict[str, Any] = field(default_factory=dict)
    description: Optional[str] = None
    condition: Optional[str] = None
    severity: str = "normal"


class RandomEventSystem:
    """System that periodically fires random events."""

    def __init__(
        self,
        events_file: str = "data/random_events.yaml",
        interval: float = 60.0,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.events_file = events_file
        self.interval = interval
        self.context: Dict[str, Any] = context or {}
        self.events: List[RandomEvent] = []
        self.weights: List[int] = []
        self.events_by_id: Dict[str, RandomEvent] = {}
        self.enabled = False
        self.task: Optional[asyncio.Task] = None

    def load_events(self) -> None:
        """Load random events from a YAML file."""
        if not Path(self.events_file).exists():
            logger.warning(f"Random events file {self.events_file} not found")
            self.events = []
            return

        try:
            with Path(self.events_file).open("r") as f:
                data = yaml.safe_load(f) or []

            self.events = []
            for evt in data:
                severity = evt.get("severity")
                if not severity:
                    severity = evt.get("params", {}).get("severity", "normal")
                self.events.append(
                    RandomEvent(
                        id=evt.get("id"),
                        name=evt.get("name", evt.get("id", "event")),
                        weight=evt.get("weight", 1),
                        params=evt.get("params", {}),
                        description=evt.get("description"),
                        condition=evt.get("condition"),
                        severity=severity,
                    )
                )
            self.weights = [evt.weight for evt in self.events]
            self.events_by_id = {evt.id: evt for evt in self.events if evt.id}
            logger.info(f"Loaded {len(self.events)} random events")
        except Exception as e:
            logger.error(f"Failed to load random events: {e}")
            self.events = []
            self.weights = []
            self.events_by_id = {}

    def start(self) -> None:
        """Start the random event loop."""
        if self.enabled:
            return
        if not self.events:
            self.load_events()
        self.enabled = True
        self.task = asyncio.create_task(self._run())
        logger.info("Random event system started")

    def stop(self) -> None:
        """Stop the random event loop."""
        self.enabled = False
        if self.task and not self.task.done():
            self.task.cancel()
        self.task = None
        logger.info("Random event system stopped")

    async def _run(self) -> None:
        while self.enabled:
            try:
                await asyncio.sleep(self.interval)
                await self.update()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in random event loop: {e}")

    async def update(self) -> None:
        """Choose and fire a random event."""
        if not self.events:
            return

        if not self.weights:
            self.weights = [evt.weight for evt in self.events]

        valid_events = [
            evt
            for evt in self.events
            if not evt.condition or self._evaluate_condition(evt.condition)
        ]
        if not valid_events:
            return

        weights = [evt.weight for evt in valid_events]
        event = random.choices(valid_events, weights=weights, k=1)[0]
        logger.debug(f"Triggering random event {event.id}")
        publish(event.id, severity=event.severity, **event.params)
        publish("random_event", event_id=event.id, event=event)

    def _evaluate_condition(self, condition: str) -> bool:
        """Safely evaluate an event condition against the current context."""
        try:
            return bool(eval(condition, {"__builtins__": {}}, self.context))  # nosec
        except Exception as e:
            logger.error(f"Failed evaluating condition '{condition}': {e}")
            return False

    def list_events(self) -> List[str]:
        """Return available event IDs."""
        return [evt.id for evt in self.events]

    def trigger_event(self, event_id: str, **kwargs: Any) -> bool:
        """Manually trigger a specific event."""
        event = self.events_by_id.get(event_id)
        if not event:
            return False
        params = {**event.params, **kwargs}
        publish(event.id, severity=event.severity, **params)
        publish("random_event", event_id=event.id, event=event)
        return True


RANDOM_EVENT_SYSTEM = RandomEventSystem()


def get_random_event_system() -> RandomEventSystem:
    """Return the global random event system instance."""
    return RANDOM_EVENT_SYSTEM
