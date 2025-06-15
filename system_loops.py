import asyncio
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)


async def run_update_loop(get_system: Callable[[], Any], interval: float = 1.0) -> None:
    """Run update loop for a subsystem."""
    system = get_system()
    system.start()
    try:
        while True:
            await asyncio.sleep(interval)
            system.update()
    except asyncio.CancelledError:
        system.stop()
        raise


async def run_forever_loop(get_system: Callable[[], Any]) -> None:
    """Run subsystem that handles its own asynchronous loop."""
    system = get_system()
    system.start()
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        system.stop()
        raise
