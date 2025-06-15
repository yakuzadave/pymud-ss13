"""Plumbing system for transferring fluids between devices."""

from __future__ import annotations

import logging
import time
from typing import Dict

from components.fluid import FluidContainerComponent

logger = logging.getLogger(__name__)


class PlumbingSystem:
    """Simple plumbing network linking containers with ducts."""

    def __init__(self, tick_interval: float = 5.0) -> None:
        self.tick_interval = tick_interval
        self.last_tick = 0.0
        self.enabled = False
        self.devices: Dict[str, FluidContainerComponent] = {}
        self.connections: Dict[str, str] = {}

    # ------------------------------------------------------------------
    def register_device(self, obj_id: str, container: FluidContainerComponent) -> None:
        self.devices[obj_id] = container

    def unregister_device(self, obj_id: str) -> None:
        self.devices.pop(obj_id, None)
        self.connections = {
            s: d for s, d in self.connections.items() if s != obj_id and d != obj_id
        }

    def connect(self, src_id: str, dst_id: str) -> None:
        self.connections[src_id] = dst_id

    def disconnect(self, src_id: str) -> None:
        self.connections.pop(src_id, None)

    def start(self) -> None:
        self.enabled = True
        self.last_tick = time.time()

    def stop(self) -> None:
        self.enabled = False

    # ------------------------------------------------------------------
    def update(self) -> None:
        if not self.enabled:
            return
        now = time.time()
        if now - self.last_tick < self.tick_interval:
            return
        self.last_tick = now
        for src_id, dst_id in list(self.connections.items()):
            src = self.devices.get(src_id)
            dst = self.devices.get(dst_id)
            if not src or not dst:
                continue
            for kind, amt in list(src.contents.items()):
                move = min(amt, dst.capacity - dst.current_volume())
                if move <= 0:
                    continue
                src.remove_fluid(kind, move)
                dst.add_fluid(kind, move)
                logger.debug(
                    "Transferred %s of %s from %s to %s", move, kind, src_id, dst_id
                )


PLUMBING_SYSTEM = PlumbingSystem()


def get_plumbing_system() -> PlumbingSystem:
    """Return the global plumbing system."""

    return PLUMBING_SYSTEM
