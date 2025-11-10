"""
Map Screen for PyMUD-SS13 TUI Client

Displays a visual grid map of the game world with navigation.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, Button
from textual import log
from rich.text import Text


class MapCell(Static):
    """A single cell in the map grid."""

    def __init__(self, cell_data: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cell_data = cell_data
        self.x = cell_data.get("x", 0)
        self.y = cell_data.get("y", 0)
        self.room_type = cell_data.get("type", "empty")
        self.is_current = cell_data.get("is_current", False)
        self.has_player = cell_data.get("has_player", False)
        self.is_visited = cell_data.get("visited", False)

    def compose(self) -> ComposeResult:
        """Compose the map cell."""
        # Determine cell character and color
        if self.has_player:
            char = "◆"
            color = "bold magenta"
        elif self.room_type == "empty":
            char = "░"
            color = "dim white"
        elif self.room_type == "wall":
            char = "█"
            color = "white"
        elif self.room_type == "door":
            char = "▢"
            color = "yellow"
        elif self.room_type == "room":
            char = "·" if self.is_visited else "○"
            color = "cyan" if self.is_visited else "dim cyan"
        elif self.room_type == "corridor":
            char = "-"
            color = "blue"
        elif self.room_type == "exit":
            char = "→"
            color = "green"
        else:
            char = "?"
            color = "white"

        # Highlight current location
        if self.is_current:
            yield Static(Text(char, style=f"bold yellow on dark_blue"))
        else:
            yield Static(Text(char, style=color))


class MapScreen(Screen):
    """Map display screen with grid visualization."""

    BINDINGS = [
        ("up", "move_north", "North"),
        ("down", "move_south", "South"),
        ("left", "move_west", "West"),
        ("right", "move_east", "East"),
        ("r", "refresh", "Refresh"),
        ("+", "zoom_in", "Zoom In"),
        ("-", "zoom_out", "Zoom Out"),
    ]

    CSS = """
    MapScreen {
        layout: vertical;
    }

    #map-main-container {
        layout: horizontal;
        height: 100%;
        padding: 1;
    }

    #map-display {
        width: 1fr;
        height: 100%;
        border: solid $primary;
        background: $surface;
        padding: 2;
    }

    .map-title {
        width: 100%;
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    #map-grid-container {
        width: 100%;
        height: 1fr;
        align: center middle;
    }

    #map-grid {
        width: auto;
        height: auto;
        background: $surface;
    }

    .map-row {
        height: auto;
        width: auto;
    }

    .map-cell {
        width: 3;
        height: 1;
        content-align: center middle;
    }

    #map-legend {
        width: 30;
        height: 100%;
        border: solid $primary;
        background: $boost;
        padding: 2;
        margin-left: 1;
    }

    .legend-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .legend-item {
        margin-bottom: 1;
    }

    .legend-symbol {
        width: 3;
        text-align: center;
        margin-right: 1;
    }

    .legend-label {
        width: 1fr;
    }

    #location-info {
        height: 8;
        border: solid $primary;
        background: $boost;
        padding: 1;
        margin-bottom: 1;
    }

    .info-row {
        height: auto;
        margin-bottom: 1;
    }

    .info-label {
        width: 12;
        color: $text-muted;
    }

    .info-value {
        width: 1fr;
        color: $text;
    }

    #navigation-controls {
        height: auto;
        border: solid $primary;
        background: $boost;
        padding: 1;
        margin-top: 1;
    }

    .nav-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
        text-align: center;
    }

    .nav-buttons {
        height: auto;
    }

    .nav-row {
        height: auto;
        align: center middle;
    }

    .nav-button {
        width: 10;
        margin: 0 1;
    }

    .map-controls {
        height: auto;
        margin-top: 1;
    }

    .control-button {
        width: 1fr;
        margin: 0 1;
    }
    """

    def __init__(self, game_client):
        super().__init__()
        self.game_client = game_client
        self.map_data = None
        self.grid_size = 15  # Default grid size
        self.player_x = 0
        self.player_y = 0
        self.current_room = "Unknown"
        self.zoom_level = 1

    def compose(self) -> ComposeResult:
        """Compose the map screen."""
        yield Header(show_clock=True)

        with Container(id="map-main-container"):
            # Main map display
            with Vertical(id="map-display"):
                yield Static("STATION MAP", classes="map-title")

                with Container(id="map-grid-container"):
                    with Vertical(id="map-grid"):
                        yield Static("Loading map...", classes="empty-message")

            # Right sidebar with legend and info
            with Vertical(id="map-legend"):
                # Location info
                with Container(id="location-info"):
                    yield Static("CURRENT LOCATION", classes="legend-title")
                    with Horizontal(classes="info-row"):
                        yield Static("Room:", classes="info-label")
                        yield Static(self.current_room, id="current-room", classes="info-value")
                    with Horizontal(classes="info-row"):
                        yield Static("Coordinates:", classes="info-label")
                        yield Static(f"({self.player_x}, {self.player_y})", id="coordinates", classes="info-value")
                    with Horizontal(classes="info-row"):
                        yield Static("Zone:", classes="info-label")
                        yield Static("Unknown", id="zone", classes="info-value")

                # Legend
                yield Static("LEGEND", classes="legend-title")
                with Vertical(classes="legend-item"):
                    with Horizontal():
                        yield Static("◆", classes="legend-symbol", styles={"color": "magenta"})
                        yield Static("Your Position", classes="legend-label")
                with Vertical(classes="legend-item"):
                    with Horizontal():
                        yield Static("·", classes="legend-symbol", styles={"color": "cyan"})
                        yield Static("Room", classes="legend-label")
                with Vertical(classes="legend-item"):
                    with Horizontal():
                        yield Static("-", classes="legend-symbol", styles={"color": "blue"})
                        yield Static("Corridor", classes="legend-label")
                with Vertical(classes="legend-item"):
                    with Horizontal():
                        yield Static("▢", classes="legend-symbol", styles={"color": "yellow"})
                        yield Static("Door", classes="legend-label")
                with Vertical(classes="legend-item"):
                    with Horizontal():
                        yield Static("█", classes="legend-symbol", styles={"color": "white"})
                        yield Static("Wall", classes="legend-label")
                with Vertical(classes="legend-item"):
                    with Horizontal():
                        yield Static("→", classes="legend-symbol", styles={"color": "green"})
                        yield Static("Exit", classes="legend-label")

                # Navigation controls
                with Container(id="navigation-controls"):
                    yield Static("NAVIGATION", classes="nav-title")
                    with Vertical(classes="nav-buttons"):
                        with Horizontal(classes="nav-row"):
                            yield Button("↑ North", id="north-btn", classes="nav-button", variant="primary")
                        with Horizontal(classes="nav-row"):
                            yield Button("← West", id="west-btn", classes="nav-button", variant="primary")
                            yield Button("↓ South", id="south-btn", classes="nav-button", variant="primary")
                            yield Button("→ East", id="east-btn", classes="nav-button", variant="primary")

                # Map controls
                with Horizontal(classes="map-controls"):
                    yield Button("Refresh", id="refresh-btn", classes="control-button", variant="success")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize when screen is mounted."""
        # Register message handlers
        self.game_client.register_handler("map", self._handle_map)
        self.game_client.register_handler("location", self._handle_location)

        # Request map data
        if self.game_client.connected:
            self.run_worker(self._request_map())

        # Load cached map if available
        cached_map = self.game_client.get_map()
        if cached_map:
            self._handle_map(cached_map)

    def on_unmount(self) -> None:
        """Cleanup when screen is unmounted."""
        self.game_client.unregister_handler("map", self._handle_map)
        self.game_client.unregister_handler("location", self._handle_location)

    async def _request_map(self):
        """Request map data from server."""
        await self.game_client.send_command("map")

    def _handle_map(self, data: dict) -> None:
        """Handle map data from server."""
        self.map_data = data
        grid = data.get("grid", [])
        self.player_x = data.get("player_x", 0)
        self.player_y = data.get("player_y", 0)

        # Update map display
        self._render_map(grid)

    def _handle_location(self, data: dict) -> None:
        """Handle location update."""
        self.current_room = data.get("name", "Unknown")
        zone = data.get("zone", "Unknown")

        # Update location info
        self.query_one("#current-room", Static).update(self.current_room)
        self.query_one("#zone", Static).update(zone)
        self.query_one("#coordinates", Static).update(f"({self.player_x}, {self.player_y})")

    def _render_map(self, grid: list):
        """Render the map grid."""
        map_grid = self.query_one("#map-grid", Vertical)
        map_grid.remove_children()

        if not grid:
            # Create a default empty grid
            grid = self._create_default_grid()

        # Render each row
        for y, row in enumerate(grid):
            row_container = Horizontal(classes="map-row")
            for x, cell_data in enumerate(row):
                # Add player marker
                if x == self.player_x and y == self.player_y:
                    cell_data["has_player"] = True
                    cell_data["is_current"] = True

                cell = MapCell(cell_data, classes="map-cell")
                row_container.compose_add_child(cell)

            map_grid.mount(row_container)

    def _create_default_grid(self) -> list:
        """Create a default empty grid."""
        grid = []
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                row.append({
                    "x": x,
                    "y": y,
                    "type": "empty",
                    "visited": False,
                    "is_current": False,
                    "has_player": False,
                })
            grid.append(row)
        return grid

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle navigation button presses."""
        button_id = event.button.id

        if button_id == "north-btn":
            await self.game_client.send_command("north")
        elif button_id == "south-btn":
            await self.game_client.send_command("south")
        elif button_id == "east-btn":
            await self.game_client.send_command("east")
        elif button_id == "west-btn":
            await self.game_client.send_command("west")
        elif button_id == "refresh-btn":
            await self._request_map()

    def action_move_north(self) -> None:
        """Move north."""
        self.query_one("#north-btn", Button).press()

    def action_move_south(self) -> None:
        """Move south."""
        self.query_one("#south-btn", Button).press()

    def action_move_west(self) -> None:
        """Move west."""
        self.query_one("#west-btn", Button).press()

    def action_move_east(self) -> None:
        """Move east."""
        self.query_one("#east-btn", Button).press()

    def action_refresh(self) -> None:
        """Refresh map data."""
        self.run_worker(self._request_map())
        self.app.notify("Refreshing map...")

    def action_zoom_in(self) -> None:
        """Zoom in on the map."""
        if self.grid_size > 7:
            self.grid_size -= 2
            self.zoom_level += 1
            self.app.notify(f"Zoom level: {self.zoom_level}")

    def action_zoom_out(self) -> None:
        """Zoom out on the map."""
        if self.grid_size < 25:
            self.grid_size += 2
            self.zoom_level -= 1
            self.app.notify(f"Zoom level: {self.zoom_level}")
