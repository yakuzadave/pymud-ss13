"""Performance monitoring and profiling utilities."""

from __future__ import annotations

import logging
import threading
import time
from contextlib import contextmanager
from typing import Dict

import psutil
import cProfile
import pstats

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Collect simple process metrics with minimal overhead."""

    def __init__(self, interval: float = 1.0) -> None:
        self.interval = interval
        self._metrics: Dict[str, float] = {}
        self._running = False
        self._thread: threading.Thread | None = None

    def _collect(self) -> None:
        process = psutil.Process()
        while self._running:
            self._metrics = {
                "cpu_percent": psutil.cpu_percent(interval=None),
                "memory_percent": process.memory_percent(),
                "num_threads": process.num_threads(),
            }
            logger.debug("Performance metrics: %s", self._metrics)
            time.sleep(self.interval)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._collect, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()

    def metrics(self) -> Dict[str, float]:
        return dict(self._metrics)


@contextmanager
def profile(section_name: str):
    """Context manager for profiling a block of code."""
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        yield
    finally:
        profiler.disable()
        stats = pstats.Stats(profiler)
        logger.debug("Profile results for %s:\n%s", section_name, stats.sort_stats("cumulative").print_stats(10))
