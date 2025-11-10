"""
Login Screen for PyMUD-SS13 TUI Client

Handles user authentication and account creation.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Static, Input, Button, Label
from textual import log


class LoginScreen(Screen):
    """Login screen for authentication."""

    CSS = """
    LoginScreen {
        align: center middle;
    }

    #login-box {
        width: 70;
        height: auto;
        border: thick $primary;
        background: $boost;
        padding: 2;
    }

    #title {
        width: 100%;
        content-align: center middle;
        text-style: bold;
        color: $accent;
        margin-bottom: 2;
    }

    .form-group {
        height: auto;
        margin-bottom: 1;
    }

    .form-label {
        width: 15;
        margin-right: 1;
        content-align: right middle;
    }

    .form-input {
        width: 1fr;
    }

    .button-row {
        height: auto;
        margin-top: 2;
        align: center middle;
    }

    Button {
        margin: 0 1;
    }

    #status-message {
        width: 100%;
        height: 3;
        content-align: center middle;
        margin-top: 1;
        color: $warning;
    }

    .ascii-art {
        width: 100%;
        content-align: center middle;
        color: $accent;
        margin-bottom: 2;
    }
    """

    def __init__(self, game_client):
        super().__init__()
        self.game_client = game_client
        self.username_input: Input = None
        self.password_input: Input = None

    def compose(self) -> ComposeResult:
        """Compose the login screen."""
        with Container(id="login-box"):
            yield Static(
                """
   ___       __  ____  ______     __________  _____
  / _ \\__ __/  |/  / / / / _ \\___/ __/ __/ |/_<  /
 / ___/ // / /|_/ / /_/ / // /___\\ \\/ _/_>  < / /
/_/   \\_, /_/  /_/\\____/____/   /___/___/_/|_/_/
     /___/
                """,
                classes="ascii-art",
            )
            yield Static("Terminal Interface", id="title")

            # Username field
            with Horizontal(classes="form-group"):
                yield Label("Username:", classes="form-label")
                yield Input(
                    placeholder="Enter username",
                    id="username-input",
                    classes="form-input",
                )

            # Password field
            with Horizontal(classes="form-group"):
                yield Label("Password:", classes="form-label")
                yield Input(
                    placeholder="Enter password",
                    password=True,
                    id="password-input",
                    classes="form-input",
                )

            # Buttons
            with Horizontal(classes="button-row"):
                yield Button("Login", id="login-btn", variant="primary")
                yield Button("New Account", id="new-account-btn", variant="default")
                yield Button("Exit", id="exit-btn", variant="error")

            # Status message
            yield Static("", id="status-message")

    def on_mount(self) -> None:
        """Initialize when screen is mounted."""
        self.username_input = self.query_one("#username-input", Input)
        self.password_input = self.query_one("#password-input", Input)
        self.username_input.focus()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "login-btn":
            await self._handle_login()
        elif button_id == "new-account-btn":
            await self._handle_new_account()
        elif button_id == "exit-btn":
            self.app.exit()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input fields."""
        if event.input.id == "username-input":
            self.password_input.focus()
        elif event.input.id == "password-input":
            await self._handle_login()

    async def _handle_login(self):
        """Handle login attempt."""
        username = self.username_input.value.strip()
        password = self.password_input.value

        if not username or not password:
            self._show_status("Please enter both username and password", "error")
            return

        self._show_status(f"Connecting as {username}...", "info")

        # Connect to server
        connected = await self.game_client.connect()

        if not connected:
            self._show_status("Failed to connect to server", "error")
            return

        # Send login command
        await self.game_client.send_command(f"login {username} {password}")

        # For now, assume success after a short delay
        # In a real implementation, you'd wait for a success/failure message from server
        import asyncio
        await asyncio.sleep(0.5)

        self._show_status("Login successful!", "success")
        await asyncio.sleep(0.5)

        # Notify the app of successful login
        await self.app.on_login_success(username)

    async def _handle_new_account(self):
        """Handle new account creation."""
        username = self.username_input.value.strip()
        password = self.password_input.value

        if not username or not password:
            self._show_status("Please enter both username and password", "error")
            return

        if len(password) < 4:
            self._show_status("Password must be at least 4 characters", "error")
            return

        self._show_status(f"Creating account for {username}...", "info")

        # Connect to server
        connected = await self.game_client.connect()

        if not connected:
            self._show_status("Failed to connect to server", "error")
            return

        # Send create account command
        await self.game_client.send_command(f"create {username} {password}")

        # For now, assume success
        import asyncio
        await asyncio.sleep(0.5)

        self._show_status("Account created! Logging in...", "success")
        await asyncio.sleep(0.5)

        # Notify the app of successful login
        await self.app.on_login_success(username)

    def _show_status(self, message: str, status_type: str = "info"):
        """Show status message."""
        status_widget = self.query_one("#status-message", Static)
        status_widget.update(message)

        # Set color based on status type
        if status_type == "error":
            status_widget.styles.color = "red"
        elif status_type == "success":
            status_widget.styles.color = "green"
        else:
            status_widget.styles.color = "yellow"
