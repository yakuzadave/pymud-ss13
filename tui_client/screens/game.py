"""
Main Game Screen for PyMUD-SS13 TUI Client

The primary game interface with terminal output, command input, and status displays.
"""

from datetime import datetime
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Static, Input, Header, Footer, RichLog
from textual import log
from rich.text import Text


class GameScreen(Screen):
    """Main game screen with terminal output and input."""

    BINDINGS = [
        ("escape", "clear_input", "Clear"),
        ("ctrl+l", "clear_log", "Clear Log"),
    ]

    CSS = """
    GameScreen {
        layout: vertical;
    }

    #game-container {
        layout: vertical;
        height: 100%;
    }

    #status-bar {
        height: 3;
        background: $boost;
        border: solid $primary;
        padding: 0 1;
    }

    .status-section {
        width: auto;
        height: 100%;
        margin-right: 2;
    }

    .status-label {
        color: $text-muted;
        margin-right: 1;
    }

    .status-value {
        color: $accent;
        text-style: bold;
    }

    #terminal-container {
        height: 1fr;
        border: solid $primary;
        background: $surface;
        margin: 1 0;
    }

    #terminal-log {
        height: 100%;
        width: 100%;
        background: $surface;
        border: none;
    }

    #input-container {
        height: auto;
        background: $boost;
        border: solid $primary;
        padding: 1;
    }

    #command-prompt {
        width: auto;
        margin-right: 1;
        color: $accent;
        text-style: bold;
    }

    #command-input {
        width: 1fr;
        border: none;
        background: $surface;
    }

    #command-input:focus {
        border: solid $accent;
    }

    .location-info {
        height: 5;
        background: $boost;
        border: solid $primary;
        padding: 1;
        margin-bottom: 1;
    }

    .location-title {
        text-style: bold;
        color: $accent;
    }
    """

    def __init__(self, game_client):
        super().__init__()
        self.game_client = game_client
        self.command_history = []
        self.history_index = 0
        self.current_location = "Unknown"
        self.player_health = 100
        self.player_status = "Healthy"

    def compose(self) -> ComposeResult:
        """Compose the game screen."""
        yield Header(show_clock=True)

        with Container(id="game-container"):
            # Status bar
            with Horizontal(id="status-bar"):
                with Horizontal(classes="status-section"):
                    yield Static("Location:", classes="status-label")
                    yield Static(self.current_location, id="status-location", classes="status-value")
                with Horizontal(classes="status-section"):
                    yield Static("Health:", classes="status-label")
                    yield Static(str(self.player_health), id="status-health", classes="status-value")
                with Horizontal(classes="status-section"):
                    yield Static("Status:", classes="status-label")
                    yield Static(self.player_status, id="status-condition", classes="status-value")
                with Horizontal(classes="status-section"):
                    yield Static("Connected:", classes="status-label")
                    yield Static("Yes" if self.game_client.connected else "No", id="status-connection", classes="status-value")

            # Current location display
            with Container(classes="location-info"):
                yield Static("Unknown Location", id="location-name", classes="location-title")
                yield Static("", id="location-description")

            # Terminal output area
            with Container(id="terminal-container"):
                yield RichLog(id="terminal-log", highlight=True, markup=True, wrap=True)

            # Command input area
            with Horizontal(id="input-container"):
                yield Static(">", id="command-prompt")
                yield Input(
                    placeholder="Enter command (type 'help' for commands)",
                    id="command-input",
                )

        yield Footer()

    def on_mount(self) -> None:
        """Initialize when screen is mounted."""
        self.command_input = self.query_one("#command-input", Input)
        self.terminal_log = self.query_one("#terminal-log", RichLog)
        self.command_input.focus()

        # Register message handlers
        self.game_client.register_handler("response", self._handle_response)
        self.game_client.register_handler("system", self._handle_system)
        self.game_client.register_handler("error", self._handle_error)
        self.game_client.register_handler("broadcast", self._handle_broadcast)
        self.game_client.register_handler("location", self._handle_location)
        self.game_client.register_handler("status", self._handle_status)

        # Welcome message
        self._add_log_entry("Welcome to PyMUD-SS13!", "system")
        self._add_log_entry("Type 'help' for available commands, or use F4 for detailed help.", "system")
        self._add_log_entry("Use F1-F4 to switch between different views.", "system")
        self._add_log_entry("-" * 60, "system")

        # Request initial state
        if self.game_client.connected:
            self.run_worker(self._request_initial_state())

    async def _request_initial_state(self):
        """Request initial game state from server."""
        await self.game_client.send_command("look")
        await self.game_client.send_command("inventory")

    def on_unmount(self) -> None:
        """Cleanup when screen is unmounted."""
        # Unregister handlers
        self.game_client.unregister_handler("response", self._handle_response)
        self.game_client.unregister_handler("system", self._handle_system)
        self.game_client.unregister_handler("error", self._handle_error)
        self.game_client.unregister_handler("broadcast", self._handle_broadcast)
        self.game_client.unregister_handler("location", self._handle_location)
        self.game_client.unregister_handler("status", self._handle_status)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle command submission."""
        if event.input.id != "command-input":
            return

        command = event.input.value.strip()
        if not command:
            return

        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)

        # Display command
        self._add_log_entry(f"> {command}", "command")

        # Send to server
        await self.game_client.send_command(command)

        # Clear input
        event.input.value = ""

    def on_key(self, event) -> None:
        """Handle keyboard events for command history."""
        if not self.command_input.has_focus:
            return

        if event.key == "up":
            # Previous command in history
            if self.history_index > 0:
                self.history_index -= 1
                self.command_input.value = self.command_history[self.history_index]
                event.prevent_default()
        elif event.key == "down":
            # Next command in history
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.command_input.value = self.command_history[self.history_index]
            elif self.history_index == len(self.command_history) - 1:
                self.history_index = len(self.command_history)
                self.command_input.value = ""
            event.prevent_default()

    def action_clear_input(self) -> None:
        """Clear the command input."""
        self.command_input.value = ""

    def action_clear_log(self) -> None:
        """Clear the terminal log."""
        self.terminal_log.clear()
        self._add_log_entry("Log cleared.", "system")

    def _handle_response(self, data: dict) -> None:
        """Handle response messages from server."""
        message = data.get("message", "")
        if message:
            self._add_log_entry(message, "response")

    def _handle_system(self, data: dict) -> None:
        """Handle system messages from server."""
        message = data.get("message", "")
        if message:
            self._add_log_entry(f"[SYSTEM] {message}", "system")

    def _handle_error(self, data: dict) -> None:
        """Handle error messages from server."""
        message = data.get("message", "")
        if message:
            self._add_log_entry(f"[ERROR] {message}", "error")

    def _handle_broadcast(self, data: dict) -> None:
        """Handle broadcast messages from server."""
        message = data.get("message", "")
        if message:
            self._add_log_entry(f"[BROADCAST] {message}", "broadcast")

    def _handle_location(self, data: dict) -> None:
        """Handle location update from server."""
        location_name = data.get("name", "Unknown")
        location_desc = data.get("description", "")

        self.current_location = location_name

        # Update status bar
        self.query_one("#status-location", Static).update(location_name)

        # Update location display
        self.query_one("#location-name", Static).update(location_name)
        self.query_one("#location-description", Static).update(location_desc)

        # Log the location change
        self._add_log_entry(f"\n=== {location_name} ===", "location")
        if location_desc:
            self._add_log_entry(location_desc, "location")

    def _handle_status(self, data: dict) -> None:
        """Handle player status updates from server."""
        if "health" in data:
            self.player_health = data["health"]
            self.query_one("#status-health", Static).update(str(self.player_health))

        if "condition" in data:
            self.player_status = data["condition"]
            self.query_one("#status-condition", Static).update(self.player_status)

        # Update connection status
        connected = "Yes" if self.game_client.connected else "No"
        self.query_one("#status-connection", Static).update(connected)

    def _add_log_entry(self, message: str, message_type: str = "normal") -> None:
        """Add an entry to the terminal log."""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Create styled text based on message type
        if message_type == "error":
            text = Text(f"[{timestamp}] {message}", style="bold red")
        elif message_type == "system":
            text = Text(f"[{timestamp}] {message}", style="yellow")
        elif message_type == "broadcast":
            text = Text(f"[{timestamp}] {message}", style="bold magenta")
        elif message_type == "location":
            text = Text(f"{message}", style="cyan")
        elif message_type == "command":
            text = Text(f"[{timestamp}] {message}", style="bold green")
        else:
            text = Text(f"[{timestamp}] {message}")

        self.terminal_log.write(text)
