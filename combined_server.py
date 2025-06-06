"""
Combined HTTP and WebSocket server for MUDpy SS13 using FastAPI.
"""

import asyncio
import logging
import os
import sys
import signal
from typing import Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from settings import settings
from server import app as api_app
from connection import ConnectionManager

# Module logger
logger = logging.getLogger(__name__)

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    """
    Handle SIGINT and SIGTERM signals for clean shutdown.
    """
    logger.info("Received shutdown signal, exiting...")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    logger.info(f"Starting MUDpy SS13 server on {settings.host}:{settings.port}")

    # Start the FastAPI server
    uvicorn.run(
        "server:app", 
        host=settings.host, 
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )
