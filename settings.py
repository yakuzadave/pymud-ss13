"""
Settings module for MUDpy SS13.
This module provides configuration settings using Pydantic.
"""

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Settings for the MUDpy server.

    These settings can be overridden by environment variables or a .env file.
    """
    host: str = "0.0.0.0"
    port: int = 5000
    # Port for WebSocket server
    ws_port: int = 8000
    # Directory for the web client
    web_client_dir: str = "web_client"
    # Configuration file
    config_file: str = "config.yaml"
    # World files
    world_rooms_file: str = "data/rooms.yaml"
    world_items_file: str = "data/items.yaml"
    # Log directory
    log_dir: str = "logs"
    # Debug mode
    debug: bool = True

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

# Create settings instance
settings = Settings()

# Ensure log directory exists
if not os.path.exists(settings.log_dir):
    os.makedirs(settings.log_dir)
