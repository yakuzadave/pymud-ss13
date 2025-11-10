"""
Help Screen for PyMUD-SS13 TUI Client

Displays command reference, keybindings, and game information.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, TabbedContent, TabPane, Markdown


class HelpScreen(Screen):
    """Help and reference screen."""

    CSS = """
    HelpScreen {
        layout: vertical;
    }

    #help-container {
        height: 100%;
        padding: 1;
    }

    TabbedContent {
        height: 100%;
        border: solid $primary;
    }

    TabPane {
        padding: 2;
    }

    .help-section {
        margin-bottom: 3;
    }

    .section-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .command-table {
        margin-left: 2;
    }

    .command-row {
        height: auto;
        margin-bottom: 1;
    }

    .command-name {
        width: 20;
        color: $success;
        text-style: bold;
    }

    .command-desc {
        width: 1fr;
        color: $text;
    }

    .keybind-row {
        height: auto;
        margin-bottom: 1;
    }

    .keybind-key {
        width: 15;
        color: $warning;
        text-style: bold;
    }

    .keybind-action {
        width: 1fr;
        color: $text;
    }

    .example-code {
        background: $boost;
        border: solid $primary;
        padding: 1;
        margin: 1 0;
        color: $success;
    }

    .tip-box {
        background: $boost;
        border: solid $accent;
        padding: 1;
        margin: 1 0;
    }

    .tip-title {
        color: $accent;
        text-style: bold;
    }
    """

    def __init__(self, game_client):
        super().__init__()
        self.game_client = game_client

    def compose(self) -> ComposeResult:
        """Compose the help screen."""
        yield Header(show_clock=True)

        with Container(id="help-container"):
            with TabbedContent():
                # Overview Tab
                with TabPane("Overview", id="overview-tab"):
                    yield self._create_overview()

                # Game Commands Tab
                with TabPane("Game Commands", id="commands-tab"):
                    yield self._create_commands()

                # Keybindings Tab
                with TabPane("Keybindings", id="keybindings-tab"):
                    yield self._create_keybindings()

                # About Tab
                with TabPane("About", id="about-tab"):
                    yield self._create_about()

        yield Footer()

    def _create_overview(self) -> VerticalScroll:
        """Create the overview content."""
        content = VerticalScroll()

        content.compose_add_child(
            Vertical(
                Static("WELCOME TO PYMUD-SS13", classes="section-title"),
                Static(
                    "PyMUD-SS13 is a Space Station 13 inspired MUD (Multi-User Dungeon) with "
                    "a full-featured terminal user interface built with Textual."
                ),
                classes="help-section"
            )
        )

        content.compose_add_child(
            Vertical(
                Static("GETTING STARTED", classes="section-title"),
                Static("1. You're currently logged in and ready to play!"),
                Static("2. Use commands in the Game view (F1) to interact with the world"),
                Static("3. Check your inventory with the Inventory view (F2)"),
                Static("4. View the station map with the Map view (F3)"),
                Static("5. Type 'look' to see your surroundings"),
                Static("6. Type 'help' in-game for a list of available commands"),
                classes="help-section"
            )
        )

        content.compose_add_child(
            Vertical(
                Static("VIEW SWITCHING", classes="section-title"),
                Static("Press function keys to switch between different views:"),
                Static(""),
                Horizontal(
                    Static("F1", classes="keybind-key"),
                    Static("Game view - Main gameplay interface", classes="keybind-action"),
                    classes="keybind-row"
                ),
                Horizontal(
                    Static("F2", classes="keybind-key"),
                    Static("Inventory view - Manage items and equipment", classes="keybind-action"),
                    classes="keybind-row"
                ),
                Horizontal(
                    Static("F3", classes="keybind-key"),
                    Static("Map view - Visual station map", classes="keybind-action"),
                    classes="keybind-row"
                ),
                Horizontal(
                    Static("F4", classes="keybind-key"),
                    Static("Help view - This screen", classes="keybind-action"),
                    classes="keybind-row"
                ),
                Horizontal(
                    Static("F10", classes="keybind-key"),
                    Static("Quit the application", classes="keybind-action"),
                    classes="keybind-row"
                ),
                classes="help-section"
            )
        )

        return content

    def _create_commands(self) -> VerticalScroll:
        """Create the game commands content."""
        content = VerticalScroll()

        # Movement commands
        content.compose_add_child(
            Vertical(
                Static("MOVEMENT COMMANDS", classes="section-title"),
                Vertical(
                    Horizontal(
                        Static("north / n", classes="command-name"),
                        Static("Move north", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("south / s", classes="command-name"),
                        Static("Move south", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("east / e", classes="command-name"),
                        Static("Move east", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("west / w", classes="command-name"),
                        Static("Move west", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("up / u", classes="command-name"),
                        Static("Move up (if available)", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("down / d", classes="command-name"),
                        Static("Move down (if available)", classes="command-desc"),
                        classes="command-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        # Interaction commands
        content.compose_add_child(
            Vertical(
                Static("INTERACTION COMMANDS", classes="section-title"),
                Vertical(
                    Horizontal(
                        Static("look / l", classes="command-name"),
                        Static("Look at your surroundings", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("examine <item>", classes="command-name"),
                        Static("Examine an item or object", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("take <item>", classes="command-name"),
                        Static("Pick up an item", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("drop <item>", classes="command-name"),
                        Static("Drop an item from inventory", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("use <item>", classes="command-name"),
                        Static("Use an item", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("equip <item>", classes="command-name"),
                        Static("Equip an item", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("unequip <item>", classes="command-name"),
                        Static("Unequip an item", classes="command-desc"),
                        classes="command-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        # Communication commands
        content.compose_add_child(
            Vertical(
                Static("COMMUNICATION COMMANDS", classes="section-title"),
                Vertical(
                    Horizontal(
                        Static("say <message>", classes="command-name"),
                        Static("Speak to others in the room", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("yell <message>", classes="command-name"),
                        Static("Yell to nearby rooms", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("whisper <message>", classes="command-name"),
                        Static("Whisper to someone nearby", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("emote <action>", classes="command-name"),
                        Static("Perform an emote action", classes="command-desc"),
                        classes="command-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        # Information commands
        content.compose_add_child(
            Vertical(
                Static("INFORMATION COMMANDS", classes="section-title"),
                Vertical(
                    Horizontal(
                        Static("inventory / i", classes="command-name"),
                        Static("View your inventory", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("status", classes="command-name"),
                        Static("View your character status", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("map", classes="command-name"),
                        Static("View the station map", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("help", classes="command-name"),
                        Static("Display help information", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("time", classes="command-name"),
                        Static("Display current game time", classes="command-desc"),
                        classes="command-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        # Station-specific commands
        content.compose_add_child(
            Vertical(
                Static("STATION-SPECIFIC COMMANDS", classes="section-title"),
                Vertical(
                    Horizontal(
                        Static("open <door/container>", classes="command-name"),
                        Static("Open a door or container", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("close <door/container>", classes="command-name"),
                        Static("Close a door or container", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("activate <device>", classes="command-name"),
                        Static("Activate a device or machine", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("deactivate <device>", classes="command-name"),
                        Static("Deactivate a device or machine", classes="command-desc"),
                        classes="command-row"
                    ),
                    Horizontal(
                        Static("repair <object>", classes="command-name"),
                        Static("Attempt to repair a damaged object", classes="command-desc"),
                        classes="command-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        return content

    def _create_keybindings(self) -> VerticalScroll:
        """Create the keybindings content."""
        content = VerticalScroll()

        # Global keybindings
        content.compose_add_child(
            Vertical(
                Static("GLOBAL KEYBINDINGS", classes="section-title"),
                Static("These keys work in all views:"),
                Static(""),
                Vertical(
                    Horizontal(
                        Static("F1", classes="keybind-key"),
                        Static("Switch to Game view", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("F2", classes="keybind-key"),
                        Static("Switch to Inventory view", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("F3", classes="keybind-key"),
                        Static("Switch to Map view", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("F4", classes="keybind-key"),
                        Static("Switch to Help view", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("F10", classes="keybind-key"),
                        Static("Quit application", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("Ctrl+C", classes="keybind-key"),
                        Static("Quit application", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        # Game view keybindings
        content.compose_add_child(
            Vertical(
                Static("GAME VIEW KEYBINDINGS", classes="section-title"),
                Vertical(
                    Horizontal(
                        Static("Up/Down", classes="keybind-key"),
                        Static("Navigate command history", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("Escape", classes="keybind-key"),
                        Static("Clear command input", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("Ctrl+L", classes="keybind-key"),
                        Static("Clear terminal log", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("Enter", classes="keybind-key"),
                        Static("Submit command", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        # Inventory view keybindings
        content.compose_add_child(
            Vertical(
                Static("INVENTORY VIEW KEYBINDINGS", classes="section-title"),
                Vertical(
                    Horizontal(
                        Static("U", classes="keybind-key"),
                        Static("Use selected item", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("E", classes="keybind-key"),
                        Static("Equip/Unequip selected item", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("D", classes="keybind-key"),
                        Static("Drop selected item", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("X", classes="keybind-key"),
                        Static("Examine selected item", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("R", classes="keybind-key"),
                        Static("Refresh inventory", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        # Map view keybindings
        content.compose_add_child(
            Vertical(
                Static("MAP VIEW KEYBINDINGS", classes="section-title"),
                Vertical(
                    Horizontal(
                        Static("Arrow Keys", classes="keybind-key"),
                        Static("Navigate in direction", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("+", classes="keybind-key"),
                        Static("Zoom in", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("-", classes="keybind-key"),
                        Static("Zoom out", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    Horizontal(
                        Static("R", classes="keybind-key"),
                        Static("Refresh map", classes="keybind-action"),
                        classes="keybind-row"
                    ),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        return content

    def _create_about(self) -> VerticalScroll:
        """Create the about content."""
        content = VerticalScroll()

        content.compose_add_child(
            Vertical(
                Static("ABOUT PYMUD-SS13", classes="section-title"),
                Static("Version: 1.0.0"),
                Static(""),
                Static(
                    "PyMUD-SS13 is a Space Station 13 inspired text-based multiplayer game "
                    "with a modern terminal user interface built using the Textual framework."
                ),
                Static(""),
                Static(
                    "This project combines the classic MUD experience with the chaotic fun "
                    "of Space Station 13, all in a beautiful terminal interface."
                ),
                classes="help-section"
            )
        )

        content.compose_add_child(
            Vertical(
                Static("TECHNOLOGY", classes="section-title"),
                Vertical(
                    Static("• Python 3.11+"),
                    Static("• Textual - Terminal UI framework"),
                    Static("• FastAPI - Backend server"),
                    Static("• WebSockets - Real-time communication"),
                    Static("• asyncio - Asynchronous processing"),
                    classes="command-table"
                ),
                classes="help-section"
            )
        )

        content.compose_add_child(
            Vertical(
                Static("TIPS & TRICKS", classes="section-title"),
                Container(
                    Static("💡 TIP", classes="tip-title"),
                    Static("Use command history with Up/Down arrows to quickly repeat commands!"),
                    classes="tip-box"
                ),
                Container(
                    Static("💡 TIP", classes="tip-title"),
                    Static("Press Tab in input fields to auto-complete common commands."),
                    classes="tip-box"
                ),
                Container(
                    Static("💡 TIP", classes="tip-title"),
                    Static("The Map view updates in real-time as you explore the station."),
                    classes="tip-box"
                ),
                Container(
                    Static("💡 TIP", classes="tip-title"),
                    Static("Click on items in the Inventory view to see detailed information."),
                    classes="tip-box"
                ),
                classes="help-section"
            )
        )

        return content
