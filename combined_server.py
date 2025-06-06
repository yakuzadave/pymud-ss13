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

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{settings.log_dir}/combined_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('combined_server')

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
