"""
Main Textual Application for PyMUD-SS13

This module contains the main TUI application with screen management
and view switching capabilities.
"""

import asyncio
from typing import Optional
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header
from textual.screen import Screen

from tui_client.screens.login import LoginScreen
from tui_client.screens.game import GameScreen
from tui_client.screens.inventory import InventoryScreen
from tui_client.screens.map import MapScreen
from tui_client.screens.help import HelpScreen
from tui_client.screens.chat import ChatScreen
from tui_client.client import GameClient


class PyMUDApp(App):
    """Main Textual application for PyMUD-SS13 with multiple switchable views."""

    CSS_PATH = "app.tcss"

    TITLE = "PyMUD-SS13 Terminal Client"
    SUB_TITLE = "A Space Station 13 MUD Experience"

    BINDINGS = [
        Binding("f1", "switch_screen('game')", "Game", show=True, priority=True),
        Binding("f2", "switch_screen('inventory')", "Inventory", show=True, priority=True),
        Binding("f3", "switch_screen('map')", "Map", show=True, priority=True),
        Binding("f4", "switch_screen('help')", "Help", show=True, priority=True),
        Binding("f5", "switch_screen('chat')", "Chat", show=True, priority=True),
        Binding("f10", "quit", "Quit", show=True, priority=True),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]

    def __init__(self, server_url: str = "ws://localhost:5000/ws", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_url = server_url
        self.game_client: Optional[GameClient] = None
        self.authenticated = False

    def on_mount(self) -> None:
        """Initialize the application and show login screen."""
        self.game_client = GameClient(self.server_url, self)
        self.push_screen(LoginScreen(self.game_client))

    async def on_login_success(self, username: str) -> None:
        """Handle successful login and switch to game screen."""
        self.authenticated = True
        self.title = f"PyMUD-SS13 - {username}"

        # Pop the login screen and push game screen
        self.pop_screen()
        await self.push_screen(GameScreen(self.game_client))

    def action_switch_screen(self, screen_name: str) -> None:
        """Switch to a different screen view."""
        if not self.authenticated:
            self.notify("Please login first", severity="warning")
            return

        # Get the current screen stack
        current_screen = self.screen

        # Don't switch if we're already on that screen
        if screen_name == "game" and isinstance(current_screen, GameScreen):
            return
        elif screen_name == "inventory" and isinstance(current_screen, InventoryScreen):
            return
        elif screen_name == "map" and isinstance(current_screen, MapScreen):
            return
        elif screen_name == "help" and isinstance(current_screen, HelpScreen):
            return
        elif screen_name == "chat" and isinstance(current_screen, ChatScreen):
            return

        # Pop current screen and push new one
        self.pop_screen()

        if screen_name == "game":
            self.push_screen(GameScreen(self.game_client))
        elif screen_name == "inventory":
            self.push_screen(InventoryScreen(self.game_client))
        elif screen_name == "map":
            self.push_screen(MapScreen(self.game_client))
        elif screen_name == "help":
            self.push_screen(HelpScreen(self.game_client))
        elif screen_name == "chat":
            self.push_screen(ChatScreen(self.game_client))

    def action_quit(self) -> None:
        """Quit the application."""
        if self.game_client:
            asyncio.create_task(self.game_client.disconnect())
        self.exit()


def run_app(server_url: str = "ws://localhost:5000/ws"):
    """Run the Textual TUI application."""
    app = PyMUDApp(server_url)
    app.run()
