#!/usr/bin/env python3
"""
Main entry point for the MUDpy WebSocket server.
This script starts the WebSocket server and a simple HTTP server for the web client.
"""

import asyncio
import logging
import os
import sys
import signal
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from mud_websocket_server import start_websocket_server
from mudpy_interface import MudpyInterface

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
logger = logging.getLogger('start_server')

# Global MudpyInterface instance for proper cleanup
mudpy_interface = None

class WebClientHandler(SimpleHTTPRequestHandler):
    """
    HTTP request handler for serving the web client.
    Serves files from the web_client directory.
    """
    def __init__(self, *args, **kwargs):
        # Set the directory to the web_client folder
        super().__init__(*args, directory='web_client', **kwargs)

def start_http_server():
    """
    Start an HTTP server for the web client.
    This runs in a separate thread.
    """
    host = '0.0.0.0'
    port = 5000
    
    logger.info(f"Starting HTTP server for web client on {host}:{port}")
    
    httpd = HTTPServer((host, port), WebClientHandler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("HTTP server stopped by user")
    finally:
        httpd.server_close()

def signal_handler(sig, frame):
    """
    Handle SIGINT and SIGTERM signals for clean shutdown.
    """
    logger.info("Received shutdown signal, cleaning up...")
    
    # Shutdown MUDpy interface
    if mudpy_interface:
        logger.info("Shutting down MUDpy interface")
        # Just release the reference, no need for a shutdown method
        # The previous line was trying to call a non-existent method
    
    sys.exit(0)

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
    
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()
    
    # Check if web_client directory exists, create it if it doesn't
    if not os.path.exists('web_client'):
        logger.warning("web_client directory not found, creating it...")
        os.makedirs('web_client')
    
    # Start WebSocket server
    await start_websocket_server()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        
        # Cleanup
        if mudpy_interface:
            logger.info("Shutting down MUDpy interface")
