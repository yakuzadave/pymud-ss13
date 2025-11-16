"""Pytest configuration and shared fixtures for the TUI tests."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest


# Ensure the repository root is importable even when ``pytest`` is invoked via
# the ``pytest`` console script, which otherwise sets ``sys.path[0]`` to the
# virtualenv's bin directory. This keeps ``import tui_client`` working for
# local smoke tests.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket connection."""
    ws = AsyncMock()
    ws.send = AsyncMock()
    ws.recv = AsyncMock()
    ws.close = AsyncMock()
    ws.closed = False
    return ws


@pytest.fixture
def mock_app():
    """Create a mock Textual app instance."""
    app = Mock()
    app.on_login_success = AsyncMock()
    app.notify = Mock()
    app.push_screen = Mock()
    app.pop_screen = Mock()
    app.exit = Mock()
    return app


@pytest.fixture
def sample_messages():
    """Provide sample WebSocket messages for testing."""
    return {
        "response": {
            "type": "response",
            "message": "You look around the room."
        },
        "system": {
            "type": "system",
            "message": "Server restarting in 5 minutes."
        },
        "error": {
            "type": "error",
            "message": "Invalid command."
        },
        "broadcast": {
            "type": "broadcast",
            "message": "New player has joined the station!"
        },
        "location": {
            "type": "location",
            "name": "Bridge",
            "description": "The command center of the station.",
            "zone": "Command",
            "exits": ["north", "south", "east", "west"]
        },
        "inventory": {
            "type": "inventory",
            "items": [
                {
                    "id": "tool_wrench_1",
                    "name": "Wrench",
                    "description": "A basic wrench for repairs.",
                    "type": "tool",
                    "weight": 0.5,
                    "quantity": 1,
                    "equipped": False
                },
                {
                    "id": "armor_helmet_1",
                    "name": "Hardhat",
                    "description": "Protects your head from falling objects.",
                    "type": "armor",
                    "weight": 1.0,
                    "quantity": 1,
                    "equipped": True
                }
            ]
        },
        "map": {
            "type": "map",
            "grid": [
                [
                    {"x": 0, "y": 0, "type": "room", "visited": True},
                    {"x": 1, "y": 0, "type": "corridor", "visited": True}
                ],
                [
                    {"x": 0, "y": 1, "type": "door", "visited": True},
                    {"x": 1, "y": 1, "type": "room", "visited": False}
                ]
            ],
            "player_x": 0,
            "player_y": 0,
            "zone": "Engineering"
        },
        "status": {
            "type": "status",
            "health": 85,
            "condition": "Bruised"
        }
    }


@pytest.fixture
def sample_commands():
    """Provide sample game commands for testing."""
    return [
        "look",
        "inventory",
        "north",
        "south",
        "east",
        "west",
        "take wrench",
        "drop helmet",
        "use medkit",
        "say hello",
        "examine door",
        "open door",
        "close door"
    ]
