#!/usr/bin/env python3
"""
Main entry point for the MUDpy combined HTTP/WebSocket server.
This script starts a WebSocket server for the MUD game and an HTTP server
for the web client, both on the same port.
"""

import asyncio
import logging
import os
import signal
import sys
from aiohttp import web
from mud_server import create_mud_server
from world import get_world
from persistence import autosave_loop
from systems import (
    get_power_system,
    get_atmos_system,
    get_random_event_system,
    get_security_system,
)




# Module logger
logger = logging.getLogger(__name__)

# Track background tasks so they can be cancelled on shutdown
TASKS: list[asyncio.Task] = []

# Create routes for the HTTP server
routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    """Serve the index.html page."""
    return web.FileResponse('web_client/index.html')

@routes.get('/{path:.+}')
async def static_files(request):
    """Serve static files."""
    path = request.match_info['path']

    if os.path.isfile(f'web_client/{path}'):
        return web.FileResponse(f'web_client/{path}')
    else:
        return web.Response(status=404, text="File not found")



async def _power_loop():
    """Run the power system update loop."""
    ps = get_power_system()
    ps.start()
    try:
        while True:
            await asyncio.sleep(1)
            ps.update()
    except asyncio.CancelledError:
        ps.stop()
        raise


async def _atmos_loop():
    """Run the atmosphere system update loop."""
    atmos = get_atmos_system()
    atmos.start()
    try:
        while True:
            await asyncio.sleep(1)
            atmos.update()
    except asyncio.CancelledError:
        atmos.stop()
        raise


async def _random_event_loop():
    """Wrapper for the random event system."""
    res = get_random_event_system()
    res.start()
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        res.stop()
        raise

async def _security_loop():
    """Run the security system update loop."""
    sec = get_security_system()
    sec.start()
    try:
        while True:
            await asyncio.sleep(1)
            sec.update()
    except asyncio.CancelledError:
        sec.stop()
        raise
async def _power_task() -> None:
    """Start and monitor the power system."""
    system = get_power_system()
    system.start()
    try:
        await asyncio.Event().wait()
    finally:
        system.stop()


async def _atmos_task() -> None:
    """Start and monitor the atmosphere system."""
    system = get_atmos_system()
    system.start()
    try:
        await asyncio.Event().wait()
    finally:
        system.stop()


async def _random_event_task() -> None:
    """Start and monitor the random event system."""
    system = get_random_event_system()
    system.start()
    try:
        await asyncio.Event().wait()
    finally:
        system.stop()

async def _security_task() -> None:
    """Start and monitor the security system."""
    system = get_security_system()
    system.start()
    try:
        while True:
            await asyncio.sleep(1)
            system.update()
    finally:
        system.stop()

def signal_handler(sig, frame):
    """
    Handle SIGINT and SIGTERM signals for clean shutdown.
    """
    logger.info("Received shutdown signal, cleaning up...")
    for task in TASKS:
        task.cancel()
    sys.exit(0)

async def main():
    """
    Main entry point for the server.
    """
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Check if web_client directory exists, create it if it doesn't
    if not os.path.exists('web_client'):
        logger.warning("web_client directory not found, creating it...")
        os.makedirs('web_client')

    # Create the MUD server
    mud_server = create_mud_server()

    # Create the app
    app = web.Application()
    app.add_routes(routes)

    # Create a task for running the MUD server
    mud_server_task = asyncio.create_task(mud_server.run())
    autosave_task = asyncio.create_task(autosave_loop(get_world(), interval=60))

    power_task = asyncio.create_task(_power_loop())
    atmos_task = asyncio.create_task(_atmos_loop())
    random_event_task = asyncio.create_task(_random_event_loop())
    security_task = asyncio.create_task(_security_loop())



    TASKS.extend([mud_server_task, autosave_task, power_task, atmos_task, random_event_task, security_task])

    # Start the HTTP server
    host = '0.0.0.0'
    port = 5000

    logger.info(f"Starting combined HTTP/WebSocket server on {host}:{port}")

    # Run the server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    get_random_event_system().start()

    # Keep the server running
    try:
        await asyncio.gather(
            mud_server_task,
            autosave_task,
            power_task,
            atmos_task,
            random_event_task,
            security_task,
            asyncio.Future()  # Run forever
        )
    except asyncio.CancelledError:
        logger.info("Server tasks cancelled")
    finally:
        get_random_event_system().stop()
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
