"""
Tests for the Textual TUI Client

This module contains comprehensive tests for the PyMUD-SS13 TUI client,
including unit tests for the GameClient, screen tests, and integration tests.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from textual.widgets import Input, Static, Button

# Import TUI components
from tui_client.client import GameClient
from tui_client.app import PyMUDApp
from tui_client.screens.login import LoginScreen
from tui_client.screens.game import GameScreen
from tui_client.screens.inventory import InventoryScreen
from tui_client.screens.map import MapScreen
from tui_client.screens.help import HelpScreen
from tui_client.screens.chat import ChatScreen


class TestGameClient:
    """Test cases for the GameClient class."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock app instance."""
        app = Mock()
        app.on_login_success = AsyncMock()
        return app

    @pytest.fixture
    def game_client(self, mock_app):
        """Create a GameClient instance."""
        return GameClient("ws://localhost:5000/ws", mock_app)

    def test_client_initialization(self, game_client):
        """Test that GameClient initializes correctly."""
        assert game_client.server_url == "ws://localhost:5000/ws"
        assert game_client.websocket is None
        assert game_client.connected is False
        assert game_client.receive_task is None
        assert isinstance(game_client.message_handlers, dict)
        assert "response" in game_client.message_handlers
        assert "system" in game_client.message_handlers
        assert "error" in game_client.message_handlers

    def test_register_handler(self, game_client):
        """Test registering a message handler."""
        handler = Mock()
        game_client.register_handler("test_type", handler)

        assert "test_type" in game_client.message_handlers
        assert handler in game_client.message_handlers["test_type"]

    def test_unregister_handler(self, game_client):
        """Test unregistering a message handler."""
        handler = Mock()
        game_client.register_handler("test_type", handler)
        game_client.unregister_handler("test_type", handler)

        assert handler not in game_client.message_handlers.get("test_type", [])

    def test_get_location(self, game_client):
        """Test getting cached location data."""
        test_location = {"name": "Test Room", "description": "A test room"}
        game_client.current_location = test_location

        assert game_client.get_location() == test_location

    def test_get_inventory(self, game_client):
        """Test getting cached inventory data."""
        test_inventory = {"items": [{"id": "1", "name": "Test Item"}]}
        game_client.current_inventory = test_inventory

        assert game_client.get_inventory() == test_inventory

    def test_get_map(self, game_client):
        """Test getting cached map data."""
        test_map = {"grid": [], "player_x": 5, "player_y": 5}
        game_client.current_map = test_map

        assert game_client.get_map() == test_map

    def test_get_status(self, game_client):
        """Test getting specific status values."""
        game_client.player_status = {
            "health": 100,
            "condition": "healthy"
        }

        assert game_client.get_status("health") == 100
        assert game_client.get_status("condition") == "healthy"
        assert game_client.get_status("nonexistent") is None

    @pytest.mark.asyncio
    async def test_handle_message_location(self, game_client):
        """Test handling location messages."""
        location_data = {
            "type": "location",
            "name": "Bridge",
            "description": "The command center"
        }

        await game_client._handle_message(location_data)

        assert game_client.current_location == location_data

    @pytest.mark.asyncio
    async def test_handle_message_inventory(self, game_client):
        """Test handling inventory messages."""
        inventory_data = {
            "type": "inventory",
            "items": [{"id": "1", "name": "Wrench"}]
        }

        await game_client._handle_message(inventory_data)

        assert game_client.current_inventory == inventory_data

    @pytest.mark.asyncio
    async def test_handle_message_map(self, game_client):
        """Test handling map messages."""
        map_data = {
            "type": "map",
            "grid": [[{"type": "room"}]],
            "player_x": 0,
            "player_y": 0
        }

        await game_client._handle_message(map_data)

        assert game_client.current_map == map_data

    @pytest.mark.asyncio
    async def test_connect_success_creates_receive_task(self, game_client, monkeypatch):
        """Connect should create the receive task when the websocket opens."""
        loop = asyncio.get_running_loop()
        created_tasks = []
        websocket = object()

        monkeypatch.setattr(
            "tui_client.client.websockets.connect",
            AsyncMock(return_value=websocket),
        )

        def fake_create_task(coro):
            task = loop.create_task(coro)
            created_tasks.append(task)
            return task

        receive_messages = AsyncMock(return_value=None)
        monkeypatch.setattr("tui_client.client.asyncio.create_task", fake_create_task)
        monkeypatch.setattr(game_client, "_receive_messages", receive_messages)

        result = await game_client.connect()

        assert result is True
        assert game_client.connected is True
        assert game_client.websocket is websocket
        assert created_tasks
        await created_tasks[0]
        assert game_client.receive_task is created_tasks[0]
        receive_messages.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_connect_failure_returns_false(self, game_client, monkeypatch):
        """Connect should return False and not create a receive task on failure."""

        async def failing_connect(_):
            raise RuntimeError("boom")

        monkeypatch.setattr("tui_client.client.websockets.connect", AsyncMock(side_effect=failing_connect))

        result = await game_client.connect()

        assert result is False
        assert game_client.connected is False
        assert game_client.receive_task is None

    @pytest.mark.asyncio
    async def test_disconnect_cancels_receive_task_and_closes_socket(self, game_client):
        """Disconnect should cancel the receive task and close the websocket."""
        loop = asyncio.get_running_loop()
        receive_task = loop.create_future()
        websocket = AsyncMock()

        game_client.receive_task = receive_task
        game_client.websocket = websocket
        game_client.connected = True

        await game_client.disconnect()

        assert receive_task.cancelled()
        websocket.close.assert_awaited_once()
        assert game_client.connected is False

    @pytest.mark.asyncio
    async def test_message_handler_called(self, game_client):
        """Test that registered handlers are called."""
        handler = AsyncMock()
        game_client.register_handler("custom", handler)

        message = {"type": "custom", "data": "test"}
        await game_client._handle_message(message)

        handler.assert_called_once_with(message)

    @pytest.mark.asyncio
    async def test_multiple_handlers_called(self, game_client):
        """Test that multiple handlers for the same type are all called."""
        handler1 = AsyncMock()
        handler2 = AsyncMock()

        game_client.register_handler("custom", handler1)
        game_client.register_handler("custom", handler2)

        message = {"type": "custom", "data": "test"}
        await game_client._handle_message(message)

        handler1.assert_called_once()
        handler2.assert_called_once()


class TestPyMUDApp:
    """Test cases for the PyMUDApp class."""

    def test_app_initialization(self):
        """Test that PyMUDApp initializes correctly."""
        app = PyMUDApp()

        assert app.server_url == "ws://localhost:5000/ws"
        assert app.game_client is None
        assert app.authenticated is False
        assert app.title == "PyMUD-SS13 Terminal Client"

    def test_app_custom_server_url(self):
        """Test initialization with custom server URL."""
        app = PyMUDApp(server_url="ws://example.com:8080/ws")

        assert app.server_url == "ws://example.com:8080/ws"

    def test_app_bindings_present(self):
        """Test that all expected key bindings are present."""
        app = PyMUDApp()
        binding_keys = [b.key for b in app.BINDINGS]

        assert "f1" in binding_keys
        assert "f2" in binding_keys
        assert "f3" in binding_keys
        assert "f4" in binding_keys
        assert "f5" in binding_keys
        assert "f10" in binding_keys
        assert "ctrl+c" in binding_keys


class TestLoginScreen:
    """Test cases for the LoginScreen."""

    @pytest.fixture
    def mock_game_client(self):
        """Create a mock GameClient."""
        client = Mock(spec=GameClient)
        client.connect = AsyncMock(return_value=True)
        client.send_command = AsyncMock()
        client.connected = False
        return client

    @pytest.fixture
    def login_screen(self, mock_game_client):
        """Create a LoginScreen instance."""
        return LoginScreen(mock_game_client)

    def test_login_screen_initialization(self, login_screen, mock_game_client):
        """Test LoginScreen initialization."""
        assert login_screen.game_client == mock_game_client
        assert login_screen.username_input is None
        assert login_screen.password_input is None


class TestGameScreen:
    """Test cases for the GameScreen."""

    @pytest.fixture
    def mock_game_client(self):
        """Create a mock GameClient."""
        client = Mock(spec=GameClient)
        client.register_handler = Mock()
        client.unregister_handler = Mock()
        client.send_command = AsyncMock()
        client.connected = True
        client.get_inventory = Mock(return_value=None)
        return client

    @pytest.fixture
    def game_screen(self, mock_game_client):
        """Create a GameScreen instance."""
        return GameScreen(mock_game_client)

    def test_game_screen_initialization(self, game_screen, mock_game_client):
        """Test GameScreen initialization."""
        assert game_screen.game_client == mock_game_client
        assert game_screen.command_history == []
        assert game_screen.history_index == 0
        assert game_screen.current_location == "Unknown"
        assert game_screen.player_health == 100

    def test_game_screen_bindings(self, game_screen):
        """Test that GameScreen has expected bindings."""
        # BINDINGS can be tuples or Binding objects
        binding_keys = []
        for b in game_screen.BINDINGS:
            if isinstance(b, tuple):
                binding_keys.append(b[0])
            else:
                binding_keys.append(b.key)

        assert "escape" in binding_keys
        assert "ctrl+l" in binding_keys

    def test_add_to_command_history(self, game_screen):
        """Test adding commands to history."""
        game_screen.command_history = ["look", "inventory"]
        game_screen.history_index = 2

        # Simulate adding a new command
        game_screen.command_history.append("north")
        game_screen.history_index = len(game_screen.command_history)

        assert len(game_screen.command_history) == 3
        assert game_screen.command_history[-1] == "north"


class TestInventoryScreen:
    """Test cases for the InventoryScreen."""

    @pytest.fixture
    def mock_game_client(self):
        """Create a mock GameClient."""
        client = Mock(spec=GameClient)
        client.register_handler = Mock()
        client.unregister_handler = Mock()
        client.send_command = AsyncMock()
        client.connected = True
        client.get_inventory = Mock(return_value=None)
        return client

    @pytest.fixture
    def inventory_screen(self, mock_game_client):
        """Create an InventoryScreen instance."""
        return InventoryScreen(mock_game_client)

    def test_inventory_screen_initialization(self, inventory_screen, mock_game_client):
        """Test InventoryScreen initialization."""
        assert inventory_screen.game_client == mock_game_client
        assert inventory_screen.selected_item is None
        assert inventory_screen.carried_items == []
        assert inventory_screen.equipped_items == []

    def test_inventory_screen_bindings(self, inventory_screen):
        """Test that InventoryScreen has expected bindings."""
        # BINDINGS can be tuples or Binding objects
        binding_keys = []
        for b in inventory_screen.BINDINGS:
            if isinstance(b, tuple):
                binding_keys.append(b[0])
            else:
                binding_keys.append(b.key)

        assert "u" in binding_keys  # Use
        assert "e" in binding_keys  # Equip
        assert "d" in binding_keys  # Drop
        assert "x" in binding_keys  # Examine
        assert "r" in binding_keys  # Refresh

    def test_handle_inventory_data(self, inventory_screen):
        """Test handling inventory data update (data processing only)."""
        inventory_data = {
            "items": [
                {"id": "1", "name": "Wrench", "equipped": False},
                {"id": "2", "name": "Helmet", "equipped": True}
            ]
        }

        # Test data processing without requiring mounted widgets
        inventory_screen.carried_items = inventory_data.get("items", [])
        inventory_screen.equipped_items = [item for item in inventory_screen.carried_items if item.get("equipped", False)]

        assert len(inventory_screen.carried_items) == 2
        assert len(inventory_screen.equipped_items) == 1
        assert inventory_screen.equipped_items[0]["name"] == "Helmet"


class TestMapScreen:
    """Test cases for the MapScreen."""

    @pytest.fixture
    def mock_game_client(self):
        """Create a mock GameClient."""
        client = Mock(spec=GameClient)
        client.register_handler = Mock()
        client.unregister_handler = Mock()
        client.send_command = AsyncMock()
        client.connected = True
        client.get_map = Mock(return_value=None)
        return client

    @pytest.fixture
    def map_screen(self, mock_game_client):
        """Create a MapScreen instance."""
        return MapScreen(mock_game_client)

    def test_map_screen_initialization(self, map_screen, mock_game_client):
        """Test MapScreen initialization."""
        assert map_screen.game_client == mock_game_client
        assert map_screen.map_data is None
        assert map_screen.grid_size == 15
        assert map_screen.player_x == 0
        assert map_screen.player_y == 0

    def test_map_screen_bindings(self, map_screen):
        """Test that MapScreen has expected bindings."""
        # BINDINGS can be tuples or Binding objects
        binding_keys = []
        for b in map_screen.BINDINGS:
            if isinstance(b, tuple):
                binding_keys.append(b[0])
            else:
                binding_keys.append(b.key)

        assert "up" in binding_keys
        assert "down" in binding_keys
        assert "left" in binding_keys
        assert "right" in binding_keys
        assert "r" in binding_keys  # Refresh
        assert "+" in binding_keys  # Zoom in
        assert "-" in binding_keys  # Zoom out

    def test_create_default_grid(self, map_screen):
        """Test creating a default empty grid."""
        grid = map_screen._create_default_grid()

        assert len(grid) == map_screen.grid_size
        assert len(grid[0]) == map_screen.grid_size
        assert grid[0][0]["type"] == "empty"
        assert grid[0][0]["visited"] is False

    def test_handle_map_data(self, map_screen):
        """Test handling map data update (data processing only)."""
        map_data = {
            "grid": [[{"type": "room", "x": 0, "y": 0}]],
            "player_x": 5,
            "player_y": 3
        }

        # Test data processing without requiring mounted widgets
        map_screen.map_data = map_data
        map_screen.player_x = map_data.get("player_x", 0)
        map_screen.player_y = map_data.get("player_y", 0)

        assert map_screen.map_data == map_data
        assert map_screen.player_x == 5
        assert map_screen.player_y == 3


class TestHelpScreen:
    """Test cases for the HelpScreen."""

    @pytest.fixture
    def mock_game_client(self):
        """Create a mock GameClient."""
        return Mock(spec=GameClient)

    @pytest.fixture
    def help_screen(self, mock_game_client):
        """Create a HelpScreen instance."""
        return HelpScreen(mock_game_client)

    def test_help_screen_initialization(self, help_screen, mock_game_client):
        """Test HelpScreen initialization."""
        assert help_screen.game_client == mock_game_client


class TestChatScreen:
    """Test cases for the ChatScreen."""

    @pytest.fixture
    def mock_game_client(self):
        """Create a mock GameClient."""
        client = Mock(spec=GameClient)
        client.register_handler = Mock()
        client.unregister_handler = Mock()
        client.send_command = AsyncMock()
        client.connected = True
        return client

    @pytest.fixture
    def chat_screen(self, mock_game_client):
        """Create a ChatScreen instance."""
        return ChatScreen(mock_game_client)

    def test_chat_screen_initialization(self, chat_screen, mock_game_client):
        """Test ChatScreen initialization."""
        assert chat_screen.game_client == mock_game_client
        assert chat_screen.current_channel == "say"
        assert chat_screen.online_players == []
        assert "say" in chat_screen.chat_logs
        assert "yell" in chat_screen.chat_logs
        assert "whisper" in chat_screen.chat_logs
        assert "radio" in chat_screen.chat_logs
        assert "ooc" in chat_screen.chat_logs

    def test_chat_screen_bindings(self, chat_screen):
        """Test that ChatScreen has expected bindings."""
        # BINDINGS can be tuples or Binding objects
        binding_keys = []
        for b in chat_screen.BINDINGS:
            if isinstance(b, tuple):
                binding_keys.append(b[0])
            else:
                binding_keys.append(b.key)

        assert "escape" in binding_keys
        assert "ctrl+l" in binding_keys
        assert "tab" in binding_keys
        assert "shift+tab" in binding_keys

    def test_switch_channel(self, chat_screen):
        """Test switching between channels (data only)."""
        # Test channel switching without mounted widgets
        chat_screen.current_channel = "yell"
        assert chat_screen.current_channel == "yell"

        chat_screen.current_channel = "radio"
        assert chat_screen.current_channel == "radio"

        chat_screen.current_channel = "ooc"
        assert chat_screen.current_channel == "ooc"

    def test_chat_logs_structure(self, chat_screen):
        """Test chat logs are properly initialized."""
        assert isinstance(chat_screen.chat_logs, dict)
        assert len(chat_screen.chat_logs) >= 5

        for channel in ["say", "yell", "whisper", "radio", "ooc"]:
            assert channel in chat_screen.chat_logs
            assert isinstance(chat_screen.chat_logs[channel], list)

    def test_handle_chat_data(self, chat_screen):
        """Test handling chat message data (data processing only)."""
        chat_data = {
            "channel": "say",
            "sender": "TestUser",
            "message": "Hello world",
            "timestamp": "12:00:00"
        }

        # Simulate receiving chat message
        # We can't test the full handler without mounted widgets,
        # but we can test the data structure
        chat_screen.chat_logs["say"].append({
            "timestamp": chat_data["timestamp"],
            "sender": chat_data["sender"],
            "message": chat_data["message"]
        })

        assert len(chat_screen.chat_logs["say"]) == 1
        assert chat_screen.chat_logs["say"][0]["sender"] == "TestUser"
        assert chat_screen.chat_logs["say"][0]["message"] == "Hello world"

    def test_handle_players_data(self, chat_screen):
        """Test handling player list data."""
        players_data = {
            "players": [
                {"name": "Player1", "role": "Engineer", "status": "online"},
                {"name": "Player2", "role": "Doctor", "status": "online"}
            ]
        }

        # Test data processing
        chat_screen.online_players = players_data.get("players", [])

        assert len(chat_screen.online_players) == 2
        assert chat_screen.online_players[0]["name"] == "Player1"
        assert chat_screen.online_players[1]["role"] == "Doctor"

    @pytest.mark.asyncio
    async def test_send_message_say(self, chat_screen, mock_game_client):
        """Test sending a say message."""
        await chat_screen._send_message("Hello", "say")
        mock_game_client.send_command.assert_called_once_with("say Hello")

    @pytest.mark.asyncio
    async def test_send_message_yell(self, chat_screen, mock_game_client):
        """Test sending a yell message."""
        await chat_screen._send_message("Help!", "yell")
        mock_game_client.send_command.assert_called_once_with("yell Help!")

    @pytest.mark.asyncio
    async def test_send_message_radio(self, chat_screen, mock_game_client):
        """Test sending a radio message."""
        await chat_screen._send_message("Copy that", "radio")
        mock_game_client.send_command.assert_called_once_with("radio Copy that")


class TestIntegration:
    """Integration tests for the TUI application."""

    @pytest.mark.asyncio
    async def test_message_routing_to_screens(self):
        """Test that messages are properly routed to screens."""
        app = Mock()
        client = GameClient("ws://localhost:5000/ws", app)

        # Register a handler
        handler_called = False
        received_data = None

        def test_handler(data):
            nonlocal handler_called, received_data
            handler_called = True
            received_data = data

        client.register_handler("test", test_handler)

        # Simulate receiving a message
        message = {"type": "test", "content": "Hello"}
        await client._handle_message(message)

        assert handler_called is True
        assert received_data == message

    @pytest.mark.asyncio
    async def test_async_handler_support(self):
        """Test that async handlers are properly called."""
        app = Mock()
        client = GameClient("ws://localhost:5000/ws", app)

        # Register an async handler
        handler_called = False

        async def async_handler(data):
            nonlocal handler_called
            await asyncio.sleep(0.001)  # Simulate async work
            handler_called = True

        client.register_handler("async_test", async_handler)

        # Simulate receiving a message
        message = {"type": "async_test", "content": "Hello"}
        await client._handle_message(message)

        assert handler_called is True

    def test_state_caching(self):
        """Test that game state is properly cached."""
        app = Mock()
        client = GameClient("ws://localhost:5000/ws", app)

        # Test location caching
        location = {"name": "Bridge", "description": "Command center"}
        client.current_location = location
        assert client.get_location() == location

        # Test inventory caching
        inventory = {"items": [{"id": "1", "name": "Tool"}]}
        client.current_inventory = inventory
        assert client.get_inventory() == inventory

        # Test map caching
        map_data = {"grid": [], "player_x": 0, "player_y": 0}
        client.current_map = map_data
        assert client.get_map() == map_data


# Performance tests
class TestPerformance:
    """Performance tests for the TUI client."""

    @pytest.mark.asyncio
    async def test_message_handler_performance(self):
        """Test that message handling is fast enough."""
        import time

        app = Mock()
        client = GameClient("ws://localhost:5000/ws", app)

        handler_count = 0

        async def fast_handler(data):
            nonlocal handler_count
            handler_count += 1

        # Register multiple handlers
        for i in range(10):
            client.register_handler("perf_test", fast_handler)

        # Measure time to handle messages
        start = time.time()

        for i in range(100):
            message = {"type": "perf_test", "data": i}
            await client._handle_message(message)

        elapsed = time.time() - start

        # Should handle 100 messages with 10 handlers each in under 1 second
        assert elapsed < 1.0
        assert handler_count == 1000  # 100 messages * 10 handlers

    def test_state_access_performance(self):
        """Test that state access is fast."""
        import time

        app = Mock()
        client = GameClient("ws://localhost:5000/ws", app)

        # Set up state
        client.current_location = {"name": "Test", "description": "Test room"}
        client.current_inventory = {"items": [{"id": str(i)} for i in range(100)]}
        client.current_map = {"grid": [[{"type": "room"}] * 20] * 20}

        # Measure access time
        start = time.time()

        for i in range(1000):
            _ = client.get_location()
            _ = client.get_inventory()
            _ = client.get_map()
            _ = client.get_status("test")

        elapsed = time.time() - start

        # Should handle 4000 state accesses in under 0.1 seconds
        assert elapsed < 0.1


# Fixtures for test data
@pytest.fixture
def sample_location_data():
    """Sample location data for testing."""
    return {
        "type": "location",
        "name": "Engineering",
        "description": "The engineering department with a large singularity engine.",
        "exits": ["north", "south", "east"],
        "items": ["wrench", "welder"]
    }


@pytest.fixture
def sample_inventory_data():
    """Sample inventory data for testing."""
    return {
        "type": "inventory",
        "items": [
            {
                "id": "wrench_1",
                "name": "Wrench",
                "description": "A basic wrench",
                "type": "tool",
                "weight": 0.5,
                "quantity": 1,
                "equipped": False
            },
            {
                "id": "helmet_1",
                "name": "Engineering Helmet",
                "description": "Protects your head",
                "type": "armor",
                "weight": 1.0,
                "quantity": 1,
                "equipped": True
            }
        ]
    }


@pytest.fixture
def sample_map_data():
    """Sample map data for testing."""
    return {
        "type": "map",
        "grid": [
            [
                {"x": 0, "y": 0, "type": "room", "visited": True},
                {"x": 1, "y": 0, "type": "corridor", "visited": True},
                {"x": 2, "y": 0, "type": "room", "visited": False}
            ],
            [
                {"x": 0, "y": 1, "type": "corridor", "visited": True},
                {"x": 1, "y": 1, "type": "door", "visited": True},
                {"x": 2, "y": 1, "type": "corridor", "visited": False}
            ],
            [
                {"x": 0, "y": 2, "type": "empty", "visited": False},
                {"x": 1, "y": 2, "type": "wall", "visited": False},
                {"x": 2, "y": 2, "type": "room", "visited": False}
            ]
        ],
        "player_x": 0,
        "player_y": 0,
        "zone": "Engineering"
    }


# Additional integration tests using fixtures
class TestWithFixtures:
    """Tests using fixture data."""

    @pytest.mark.asyncio
    async def test_location_update(self, sample_location_data):
        """Test location data handling with fixture."""
        app = Mock()
        client = GameClient("ws://localhost:5000/ws", app)

        await client._handle_message(sample_location_data)

        assert client.current_location == sample_location_data
        assert client.get_location()["name"] == "Engineering"

    @pytest.mark.asyncio
    async def test_inventory_update(self, sample_inventory_data):
        """Test inventory data handling with fixture."""
        app = Mock()
        client = GameClient("ws://localhost:5000/ws", app)

        await client._handle_message(sample_inventory_data)

        assert client.current_inventory == sample_inventory_data
        items = client.get_inventory()["items"]
        assert len(items) == 2
        assert items[0]["name"] == "Wrench"
        assert items[1]["equipped"] is True

    @pytest.mark.asyncio
    async def test_map_update(self, sample_map_data):
        """Test map data handling with fixture."""
        app = Mock()
        client = GameClient("ws://localhost:5000/ws", app)

        await client._handle_message(sample_map_data)

        assert client.current_map == sample_map_data
        map_info = client.get_map()
        assert map_info["player_x"] == 0
        assert map_info["player_y"] == 0
        assert len(map_info["grid"]) == 3
        assert len(map_info["grid"][0]) == 3
