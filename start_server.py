#!/usr/bin/env python3
"""
Main entry point for the MUDpy WebSocket server.
This script starts a combined HTTP and WebSocket server on the same port.
"""

import asyncio
import logging
import os
import sys
import signal
import json
from aiohttp import web
from mud_websocket_server import handle_client, active_clients
from mudpy_interface import MudpyInterface
import integration
import engine
from systems import (
    get_power_system,
    get_atmos_system,
    get_random_event_system,
    get_security_system,
)

# Import command modules to ensure handlers are registered
from commands import basic, movement, inventory, system, interaction

# Configure more detailed logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Track background tasks to cancel on shutdown
TASKS: list[asyncio.Task] = []

# Global MudpyInterface instance for proper cleanup
mudpy_interface = None

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


def signal_handler(sig, frame):
    """
    Handle SIGINT and SIGTERM signals for clean shutdown.
    """
    logger.info("Received shutdown signal, cleaning up...")

    for task in TASKS:
        task.cancel()

    # Shutdown MUDpy interface
    if mudpy_interface:
        logger.info("Shutting down MUDpy interface")
        try:
            mudpy_interface.shutdown()
        except AttributeError:
            # No shutdown method, just let it be garbage collected
            pass

    sys.exit(0)

async def on_shutdown(app):
    """Handle graceful shutdown."""
    for ws in active_clients.values():
        await ws.close(code=1001, reason="Server shutdown")
    for task in TASKS:
        task.cancel()

async def websocket_handler(request):
    """Handle WebSocket connections."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    logger.info(f"WebSocket connection established: {id(ws)}")

    # Process WebSocket connection using our existing handler
    try:
        await handle_client(ws)
    except Exception as e:
        logger.error(f"Error in WebSocket handler: {e}")

    return ws

async def main():
    """
    Main entry point for the server.
    """
    global mudpy_interface

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create MudpyInterface instance
    mudpy_interface = MudpyInterface()

    # Create the integration with the new engine architecture
    mud_integration = integration.create_integration(mudpy_interface)

    # Check if web_client directory exists, create it if it doesn't
    if not os.path.exists('web_client'):
        logger.warning("web_client directory not found, creating it...")
        os.makedirs('web_client')

    # Create the app
    app = web.Application()
    app.add_routes(routes)

    # Add WebSocket route
    app.router.add_get('/ws', websocket_handler)

    # Add shutdown handler
    app.on_shutdown.append(on_shutdown)

    # Background subsystem tasks

    power_task = asyncio.create_task(_power_loop())
    atmos_task = asyncio.create_task(_atmos_loop())
    random_event_task = asyncio.create_task(_random_event_loop())
    security_task = asyncio.create_task(_security_loop())

    TASKS.extend([power_task, atmos_task, random_event_task, security_task])

    # Start the server
    host = '0.0.0.0'
    port = 5000

    logger.info(f"Starting combined HTTP/WebSocket server on {host}:{port}")

    # Run the server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    # Keep the server running
    try:
        await asyncio.gather(
            power_task,
            atmos_task,
            random_event_task,
            security_task,
            asyncio.Future(),
        )
    except asyncio.CancelledError:
        logger.info("Server tasks cancelled")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")

        # Cleanup
        if mudpy_interface:
            logger.info("Shutting down MUDpy interface")
            try:
                mudpy_interface.shutdown()
            except AttributeError:
                pass
