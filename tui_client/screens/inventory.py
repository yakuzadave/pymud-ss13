"""
Inventory Screen for PyMUD-SS13 TUI Client

Displays player inventory, equipment, and item management.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, Button, ListView, ListItem, Label
from textual.message import Message
from textual import log
from rich.text import Text


class ItemWidget(Static):
    """Widget representing a single item."""

    class ItemSelected(Message):
        """Message when an item is selected."""

        def __init__(self, item_widget):
            super().__init__()
            self.item_widget = item_widget

    def __init__(self, item_data: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_data = item_data
        self.item_id = item_data.get("id", "unknown")
        self.item_name = item_data.get("name", "Unknown Item")
        self.item_desc = item_data.get("description", "")
        self.is_equipped = item_data.get("equipped", False)
        self.quantity = item_data.get("quantity", 1)

    def compose(self) -> ComposeResult:
        """Compose the item widget."""
        # Create display text
        equipped_marker = "⚡" if self.is_equipped else "  "
        quantity_text = f" x{self.quantity}" if self.quantity > 1 else ""

        with Horizontal():
            yield Static(equipped_marker, classes="item-equipped-marker")
            yield Static(f"{self.item_name}{quantity_text}", classes="item-name")

    def on_click(self) -> None:
        """Handle item click."""
        self.post_message(self.ItemSelected(self))


class InventoryScreen(Screen):
    """Inventory management screen."""

    BINDINGS = [
        ("u", "use_item", "Use"),
        ("e", "equip_item", "Equip"),
        ("d", "drop_item", "Drop"),
        ("x", "examine_item", "Examine"),
        ("r", "refresh", "Refresh"),
    ]

    CSS = """
    InventoryScreen {
        layout: vertical;
    }

    #inventory-container {
        layout: horizontal;
        height: 100%;
        padding: 1;
    }

    #left-panel {
        width: 1fr;
        height: 100%;
    }

    #right-panel {
        width: 40;
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

    #carried-items-list {
        height: 1fr;
        border: solid $primary;
        background: $surface;
        margin-bottom: 1;
    }

    #equipped-items-list {
        height: 1fr;
        border: solid $primary;
        background: $surface;
    }

    .item-container {
        padding: 1;
        margin: 1;
        border: solid $primary;
        background: $panel;
    }

    .item-container:hover {
        background: $boost;
        border: solid $accent;
    }

    .item-container-selected {
        background: $accent;
        border: solid $accent;
    }

    .item-equipped-marker {
        width: 3;
        color: $success;
        text-style: bold;
    }

    .item-name {
        width: 1fr;
        color: $text;
    }

    #item-details {
        border: solid $primary;
        background: $boost;
        padding: 2;
        height: 1fr;
    }

    .detail-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .detail-section {
        margin-bottom: 1;
    }

    .detail-label {
        color: $text-muted;
    }

    .detail-value {
        color: $text;
        margin-left: 1;
    }

    #item-actions {
        height: auto;
        border: solid $primary;
        background: $boost;
        padding: 1;
        margin-top: 1;
    }

    .action-button {
        width: 1fr;
        margin: 0 1;
    }

    #stats-panel {
        height: 12;
        border: solid $primary;
        background: $boost;
        padding: 1;
        margin-top: 1;
    }

    .stat-row {
        height: auto;
        margin-bottom: 1;
    }

    .empty-message {
        width: 100%;
        height: 100%;
        content-align: center middle;
        color: $text-muted;
        text-style: italic;
    }
    """

    def __init__(self, game_client):
        super().__init__()
        self.game_client = game_client
        self.selected_item = None
        self.carried_items = []
        self.equipped_items = []

    def compose(self) -> ComposeResult:
        """Compose the inventory screen."""
        yield Header(show_clock=True)

        with Container(id="inventory-container"):
            # Left panel - item lists
            with Vertical(id="left-panel"):
                yield Static("CARRIED ITEMS", classes="panel-title")
                with VerticalScroll(id="carried-items-list"):
                    yield Static("Loading inventory...", classes="empty-message")

                yield Static("EQUIPPED ITEMS", classes="panel-title")
                with VerticalScroll(id="equipped-items-list"):
                    yield Static("No items equipped", classes="empty-message")

            # Right panel - details and actions
            with Vertical(id="right-panel"):
                yield Static("ITEM DETAILS", classes="panel-title")

                with VerticalScroll(id="item-details"):
                    yield Static("Select an item to view details", classes="empty-message")

                with Horizontal(id="item-actions"):
                    yield Button("Use", id="use-btn", classes="action-button", variant="primary")
                    yield Button("Equip", id="equip-btn", classes="action-button", variant="success")
                    yield Button("Drop", id="drop-btn", classes="action-button", variant="error")

                with Container(id="stats-panel"):
                    yield Static("PLAYER STATS", classes="detail-title")
                    with Horizontal(classes="stat-row"):
                        yield Static("Total Weight:", classes="detail-label")
                        yield Static("0 kg", id="total-weight", classes="detail-value")
                    with Horizontal(classes="stat-row"):
                        yield Static("Carrying Capacity:", classes="detail-label")
                        yield Static("50 kg", id="max-weight", classes="detail-value")
                    with Horizontal(classes="stat-row"):
                        yield Static("Item Count:", classes="detail-label")
                        yield Static("0", id="item-count", classes="detail-value")
                    with Horizontal(classes="stat-row"):
                        yield Static("Credits:", classes="detail-label")
                        yield Static("0", id="credits", classes="detail-value")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize when screen is mounted."""
        # Register message handler
        self.game_client.register_handler("inventory", self._handle_inventory)

        # Request inventory data
        if self.game_client.connected:
            self.run_worker(self._request_inventory())

        # Load cached inventory if available
        cached_inventory = self.game_client.get_inventory()
        if cached_inventory:
            self._handle_inventory(cached_inventory)

    def on_unmount(self) -> None:
        """Cleanup when screen is unmounted."""
        self.game_client.unregister_handler("inventory", self._handle_inventory)

    async def _request_inventory(self):
        """Request inventory data from server."""
        await self.game_client.send_command("inventory")

    def _handle_inventory(self, data: dict) -> None:
        """Handle inventory data from server."""
        # Parse inventory data
        self.carried_items = data.get("items", [])
        self.equipped_items = [item for item in self.carried_items if item.get("equipped", False)]

        # Update displays
        self._update_carried_items()
        self._update_equipped_items()
        self._update_stats()

    def _update_carried_items(self):
        """Update the carried items list."""
        carried_list = self.query_one("#carried-items-list", VerticalScroll)
        carried_list.remove_children()

        if not self.carried_items:
            carried_list.mount(Static("No items in inventory", classes="empty-message"))
            return

        for item in self.carried_items:
            if not item.get("equipped", False):
                item_widget = ItemWidget(item, classes="item-container")
                carried_list.mount(item_widget)

    def _update_equipped_items(self):
        """Update the equipped items list."""
        equipped_list = self.query_one("#equipped-items-list", VerticalScroll)
        equipped_list.remove_children()

        if not self.equipped_items:
            equipped_list.mount(Static("No items equipped", classes="empty-message"))
            return

        for item in self.equipped_items:
            item_widget = ItemWidget(item, classes="item-container")
            equipped_list.mount(item_widget)

    def _update_stats(self):
        """Update player stats display."""
        total_weight = sum(item.get("weight", 0) * item.get("quantity", 1) for item in self.carried_items)
        item_count = len(self.carried_items)

        self.query_one("#total-weight", Static).update(f"{total_weight:.1f} kg")
        self.query_one("#item-count", Static).update(str(item_count))

    def _select_item(self, item_widget: ItemWidget):
        """Select an item and show its details."""
        self.selected_item = item_widget.item_data

        # Update details panel
        details_panel = self.query_one("#item-details", VerticalScroll)
        details_panel.remove_children()

        name = self.selected_item.get("name", "Unknown")
        desc = self.selected_item.get("description", "No description")
        weight = self.selected_item.get("weight", 0)
        quantity = self.selected_item.get("quantity", 1)
        item_type = self.selected_item.get("type", "item")
        equipped = self.selected_item.get("equipped", False)

        # Build details view
        details_content = Container(
            Static(name, classes="detail-title"),
            Static(desc, classes="detail-section"),
            Horizontal(
                Static("Type:", classes="detail-label"),
                Static(item_type, classes="detail-value"),
                classes="detail-section"
            ),
            Horizontal(
                Static("Weight:", classes="detail-label"),
                Static(f"{weight} kg", classes="detail-value"),
                classes="detail-section"
            ),
            Horizontal(
                Static("Quantity:", classes="detail-label"),
                Static(str(quantity), classes="detail-value"),
                classes="detail-section"
            ),
            Horizontal(
                Static("Status:", classes="detail-label"),
                Static("Equipped" if equipped else "In Inventory", classes="detail-value"),
                classes="detail-section"
            ),
        )

        details_panel.mount(details_content)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle action button presses."""
        if not self.selected_item:
            self.app.notify("No item selected", severity="warning")
            return

        item_id = self.selected_item.get("id", "")
        item_name = self.selected_item.get("name", "item")

        if event.button.id == "use-btn":
            await self.game_client.send_command(f"use {item_id}")
            self.app.notify(f"Using {item_name}")
        elif event.button.id == "equip-btn":
            if self.selected_item.get("equipped", False):
                await self.game_client.send_command(f"unequip {item_id}")
                self.app.notify(f"Unequipping {item_name}")
            else:
                await self.game_client.send_command(f"equip {item_id}")
                self.app.notify(f"Equipping {item_name}")
        elif event.button.id == "drop-btn":
            await self.game_client.send_command(f"drop {item_id}")
            self.app.notify(f"Dropping {item_name}")

    def on_item_widget_item_selected(self, message: ItemWidget.ItemSelected) -> None:
        """Handle item selection."""
        self._select_item(message.item_widget)

    def action_use_item(self) -> None:
        """Use the selected item."""
        if self.selected_item:
            self.query_one("#use-btn", Button).press()

    def action_equip_item(self) -> None:
        """Equip/unequip the selected item."""
        if self.selected_item:
            self.query_one("#equip-btn", Button).press()

    def action_drop_item(self) -> None:
        """Drop the selected item."""
        if self.selected_item:
            self.query_one("#drop-btn", Button).press()

    def action_examine_item(self) -> None:
        """Examine the selected item."""
        if self.selected_item:
            item_id = self.selected_item.get("id", "")
            self.run_worker(self.game_client.send_command(f"examine {item_id}"))

    def action_refresh(self) -> None:
        """Refresh inventory data."""
        self.run_worker(self._request_inventory())
        self.app.notify("Refreshing inventory...")
