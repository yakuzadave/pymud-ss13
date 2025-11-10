"""
Chat Screen for PyMUD-SS13 TUI Client

Provides a dedicated communication interface with multiple chat channels,
player list, and message history.
"""

from datetime import datetime
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, Input, Button, TabbedContent, TabPane, RichLog
from textual import log
from rich.text import Text


class PlayerListItem(Static):
    """Widget representing a player in the online list."""

    def __init__(self, player_data: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_name = player_data.get("name", "Unknown")
        self.player_role = player_data.get("role", "")
        self.player_status = player_data.get("status", "online")

    def compose(self) -> ComposeResult:
        """Compose the player list item."""
        status_indicator = "●" if self.player_status == "online" else "○"
        role_text = f" [{self.player_role}]" if self.player_role else ""

        yield Static(
            f"{status_indicator} {self.player_name}{role_text}",
            classes="player-item"
        )


class ChatScreen(Screen):
    """Chat and communication screen with multiple channels."""

    BINDINGS = [
        ("escape", "clear_input", "Clear"),
        ("ctrl+l", "clear_channel", "Clear Channel"),
        ("tab", "next_channel", "Next Channel"),
        ("shift+tab", "prev_channel", "Prev Channel"),
    ]

    CSS = """
    ChatScreen {
        layout: vertical;
    }

    #chat-container {
        layout: horizontal;
        height: 100%;
        padding: 1;
    }

    #chat-main {
        width: 1fr;
        height: 100%;
    }

    #chat-sidebar {
        width: 30;
        height: 100%;
        margin-left: 1;
    }

    .panel-title {
        background: $primary;
        color: $text;
        text-style: bold;
        padding: 1;
        text-align: center;
    }

    #channel-tabs {
        height: 1fr;
        border: solid $primary;
        background: $surface;
        margin-bottom: 1;
    }

    TabPane {
        padding: 0;
    }

    .chat-log {
        height: 100%;
        width: 100%;
        padding: 1;
        background: $surface;
        scrollbar-background: $panel;
        scrollbar-color: $primary;
    }

    #chat-input-container {
        height: auto;
        background: $boost;
        border: solid $primary;
        padding: 1;
    }

    #channel-indicator {
        width: auto;
        margin-right: 1;
        color: $accent;
        text-style: bold;
    }

    #chat-input {
        width: 1fr;
        border: none;
        background: $surface;
    }

    #chat-input:focus {
        border: solid $accent;
    }

    #players-panel {
        height: 1fr;
        border: solid $primary;
        background: $boost;
        margin-bottom: 1;
    }

    #player-list {
        height: 1fr;
        padding: 1;
    }

    .player-item {
        padding: 0 1;
        margin-bottom: 0;
    }

    .player-item:hover {
        background: $primary;
    }

    #player-count {
        padding: 1;
        text-align: center;
        color: $text-muted;
        border-top: solid $primary;
    }

    #channel-controls {
        height: auto;
        border: solid $primary;
        background: $boost;
        padding: 1;
    }

    .control-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .control-row {
        height: auto;
        margin-bottom: 1;
    }

    .control-button {
        width: 1fr;
        margin: 0 1;
    }

    .chat-message-say {
        color: $text;
    }

    .chat-message-yell {
        color: red;
        text-style: bold;
    }

    .chat-message-whisper {
        color: cyan;
        text-style: italic;
    }

    .chat-message-radio {
        color: green;
    }

    .chat-message-ooc {
        color: yellow;
    }

    .chat-message-system {
        color: $warning;
        text-style: italic;
    }
    """

    def __init__(self, game_client):
        super().__init__()
        self.game_client = game_client
        self.current_channel = "say"
        self.online_players = []

        # Chat logs for each channel
        self.chat_logs = {
            "say": [],
            "yell": [],
            "whisper": [],
            "radio": [],
            "ooc": [],
            "system": []
        }

    def compose(self) -> ComposeResult:
        """Compose the chat screen."""
        yield Header(show_clock=True)

        with Container(id="chat-container"):
            # Main chat area
            with Vertical(id="chat-main"):
                yield Static("COMMUNICATIONS", classes="panel-title")

                # Channel tabs
                with TabbedContent(id="channel-tabs"):
                    with TabPane("Say", id="say-tab"):
                        yield RichLog(
                            id="say-log",
                            classes="chat-log",
                            highlight=True,
                            markup=True,
                            wrap=True
                        )

                    with TabPane("Yell", id="yell-tab"):
                        yield RichLog(
                            id="yell-log",
                            classes="chat-log",
                            highlight=True,
                            markup=True,
                            wrap=True
                        )

                    with TabPane("Whisper", id="whisper-tab"):
                        yield RichLog(
                            id="whisper-log",
                            classes="chat-log",
                            highlight=True,
                            markup=True,
                            wrap=True
                        )

                    with TabPane("Radio", id="radio-tab"):
                        yield RichLog(
                            id="radio-log",
                            classes="chat-log",
                            highlight=True,
                            markup=True,
                            wrap=True
                        )

                    with TabPane("OOC", id="ooc-tab"):
                        yield RichLog(
                            id="ooc-log",
                            classes="chat-log",
                            highlight=True,
                            markup=True,
                            wrap=True
                        )

                    with TabPane("System", id="system-tab"):
                        yield RichLog(
                            id="system-log",
                            classes="chat-log",
                            highlight=True,
                            markup=True,
                            wrap=True
                        )

                # Chat input
                with Horizontal(id="chat-input-container"):
                    yield Static("[SAY]", id="channel-indicator")
                    yield Input(
                        placeholder="Type your message... (Tab to switch channels)",
                        id="chat-input",
                    )

            # Sidebar
            with Vertical(id="chat-sidebar"):
                # Player list
                with Container(id="players-panel"):
                    yield Static("ONLINE PLAYERS", classes="panel-title")
                    with VerticalScroll(id="player-list"):
                        yield Static("Loading...", classes="player-item")
                    yield Static("Players: 0", id="player-count")

                # Channel controls
                with Container(id="channel-controls"):
                    yield Static("QUICK ACTIONS", classes="control-title")
                    with Horizontal(classes="control-row"):
                        yield Button("Say", id="say-btn", classes="control-button", variant="primary")
                        yield Button("Yell", id="yell-btn", classes="control-button", variant="warning")
                    with Horizontal(classes="control-row"):
                        yield Button("Whisper", id="whisper-btn", classes="control-button", variant="default")
                        yield Button("Radio", id="radio-btn", classes="control-button", variant="success")
                    with Horizontal(classes="control-row"):
                        yield Button("OOC", id="ooc-btn", classes="control-button", variant="default")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize when screen is mounted."""
        self.chat_input = self.query_one("#chat-input", Input)
        self.chat_input.focus()

        # Register message handlers
        self.game_client.register_handler("chat", self._handle_chat)
        self.game_client.register_handler("players", self._handle_players)
        self.game_client.register_handler("system", self._handle_system_message)

        # Welcome message
        self._add_system_message("Welcome to the communications interface!")
        self._add_system_message("Use Tab to switch between channels.")
        self._add_system_message("Type '/help' for a list of chat commands.")

        # Request player list
        if self.game_client.connected:
            self.run_worker(self.game_client.send_command("who"))

    def on_unmount(self) -> None:
        """Cleanup when screen is unmounted."""
        self.game_client.unregister_handler("chat", self._handle_chat)
        self.game_client.unregister_handler("players", self._handle_players)
        self.game_client.unregister_handler("system", self._handle_system_message)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle message submission."""
        if event.input.id != "chat-input":
            return

        message = event.input.value.strip()
        if not message:
            return

        # Check for slash commands
        if message.startswith("/"):
            await self._handle_slash_command(message)
        else:
            # Send message in current channel
            await self._send_message(message, self.current_channel)

        # Clear input
        event.input.value = ""

    async def _handle_slash_command(self, command: str):
        """Handle slash commands."""
        parts = command[1:].split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "help":
            self._add_system_message("Available commands:")
            self._add_system_message("  /say <message> - Say something")
            self._add_system_message("  /yell <message> - Yell something")
            self._add_system_message("  /whisper <player> <message> - Whisper to someone")
            self._add_system_message("  /radio <message> - Send radio message")
            self._add_system_message("  /ooc <message> - Out of character chat")
            self._add_system_message("  /who - List online players")
            self._add_system_message("  /clear - Clear current channel")
        elif cmd == "say":
            await self._send_message(args, "say")
        elif cmd == "yell":
            await self._send_message(args, "yell")
        elif cmd == "whisper":
            whisper_parts = args.split(maxsplit=1)
            if len(whisper_parts) < 2:
                self._add_system_message("Usage: /whisper <player> <message>")
            else:
                await self.game_client.send_command(f"whisper {whisper_parts[0]} {whisper_parts[1]}")
        elif cmd == "radio":
            await self._send_message(args, "radio")
        elif cmd == "ooc":
            await self._send_message(args, "ooc")
        elif cmd == "who":
            await self.game_client.send_command("who")
        elif cmd == "clear":
            self._clear_current_channel()
        else:
            self._add_system_message(f"Unknown command: {cmd}. Type /help for available commands.")

    async def _send_message(self, message: str, channel: str):
        """Send a message to the specified channel."""
        if not message:
            return

        # Map channel to game command
        command_map = {
            "say": f"say {message}",
            "yell": f"yell {message}",
            "radio": f"radio {message}",
            "ooc": f"ooc {message}",
            "whisper": f"whisper {message}"
        }

        command = command_map.get(channel, f"say {message}")
        await self.game_client.send_command(command)

    def _handle_chat(self, data: dict) -> None:
        """Handle incoming chat messages."""
        channel = data.get("channel", "say")
        sender = data.get("sender", "Unknown")
        message = data.get("message", "")
        timestamp = data.get("timestamp", datetime.now().strftime("%H:%M:%S"))

        self._add_chat_message(channel, sender, message, timestamp)

    def _handle_players(self, data: dict) -> None:
        """Handle player list update."""
        players = data.get("players", [])
        self.online_players = players
        self._update_player_list()

    def _handle_system_message(self, data: dict) -> None:
        """Handle system messages."""
        message = data.get("message", "")
        if message:
            self._add_system_message(message)

    def _add_chat_message(self, channel: str, sender: str, message: str, timestamp: str = None):
        """Add a message to the specified channel."""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M:%S")

        # Get the log for this channel
        log_id = f"{channel}-log"
        try:
            chat_log = self.query_one(f"#{log_id}", RichLog)
        except:
            log(f"Warning: Could not find log for channel {channel}")
            return

        # Format message based on channel
        if channel == "say":
            text = Text(f"[{timestamp}] {sender} says: {message}", style="white")
        elif channel == "yell":
            text = Text(f"[{timestamp}] {sender} yells: {message}", style="bold red")
        elif channel == "whisper":
            text = Text(f"[{timestamp}] {sender} whispers: {message}", style="italic cyan")
        elif channel == "radio":
            text = Text(f"[{timestamp}] {sender} (radio): {message}", style="green")
        elif channel == "ooc":
            text = Text(f"[{timestamp}] [OOC] {sender}: {message}", style="yellow")
        else:
            text = Text(f"[{timestamp}] {sender}: {message}")

        chat_log.write(text)

        # Store in log
        if channel in self.chat_logs:
            self.chat_logs[channel].append({
                "timestamp": timestamp,
                "sender": sender,
                "message": message
            })

    def _add_system_message(self, message: str):
        """Add a system message to all relevant logs."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        text = Text(f"[{timestamp}] [SYSTEM] {message}", style="italic yellow")

        # Add to system log
        try:
            system_log = self.query_one("#system-log", RichLog)
            system_log.write(text)
        except:
            pass

    def _update_player_list(self):
        """Update the online player list."""
        player_list = self.query_one("#player-list", VerticalScroll)
        player_list.remove_children()

        if not self.online_players:
            player_list.mount(Static("No players online", classes="player-item"))
        else:
            for player in self.online_players:
                player_widget = PlayerListItem(player, classes="player-item")
                player_list.mount(player_widget)

        # Update count
        count_widget = self.query_one("#player-count", Static)
        count_widget.update(f"Players: {len(self.online_players)}")

    def _switch_channel(self, channel: str):
        """Switch to a different channel."""
        self.current_channel = channel

        # Update channel indicator
        channel_indicator = self.query_one("#channel-indicator", Static)
        channel_map = {
            "say": "[SAY]",
            "yell": "[YELL]",
            "whisper": "[WHISPER]",
            "radio": "[RADIO]",
            "ooc": "[OOC]"
        }
        channel_indicator.update(channel_map.get(channel, "[SAY]"))

        # Update input placeholder
        self.chat_input.placeholder = f"Type your {channel} message..."

    def _clear_current_channel(self):
        """Clear the current channel's log."""
        log_id = f"{self.current_channel}-log"
        try:
            chat_log = self.query_one(f"#{log_id}", RichLog)
            chat_log.clear()
            self._add_system_message(f"Cleared {self.current_channel} channel")
        except:
            pass

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle channel button presses."""
        button_id = event.button.id

        if button_id == "say-btn":
            self._switch_channel("say")
            self.app.notify("Switched to Say channel")
        elif button_id == "yell-btn":
            self._switch_channel("yell")
            self.app.notify("Switched to Yell channel")
        elif button_id == "whisper-btn":
            self._switch_channel("whisper")
            self.app.notify("Switched to Whisper channel")
        elif button_id == "radio-btn":
            self._switch_channel("radio")
            self.app.notify("Switched to Radio channel")
        elif button_id == "ooc-btn":
            self._switch_channel("ooc")
            self.app.notify("Switched to OOC channel")

    def action_clear_input(self) -> None:
        """Clear the chat input."""
        self.chat_input.value = ""

    def action_clear_channel(self) -> None:
        """Clear the current channel."""
        self._clear_current_channel()

    def action_next_channel(self) -> None:
        """Switch to the next channel."""
        channels = ["say", "yell", "whisper", "radio", "ooc"]
        try:
            current_index = channels.index(self.current_channel)
            next_index = (current_index + 1) % len(channels)
            self._switch_channel(channels[next_index])
        except ValueError:
            self._switch_channel("say")

    def action_prev_channel(self) -> None:
        """Switch to the previous channel."""
        channels = ["say", "yell", "whisper", "radio", "ooc"]
        try:
            current_index = channels.index(self.current_channel)
            prev_index = (current_index - 1) % len(channels)
            self._switch_channel(channels[prev_index])
        except ValueError:
            self._switch_channel("say")
