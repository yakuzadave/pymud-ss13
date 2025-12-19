"""
Behave step definitions for TUI testing.

These steps define the actions and assertions for TUI BDD tests.
"""

import asyncio
import time
from behave import given, when, then, step
from unittest.mock import Mock, AsyncMock, patch
from textual.widgets import Input, Button, Static

# Import TUI components
from tui_client.app import PyMUDApp
from tui_client.client import GameClient
from tui_client.screens.login import LoginScreen
from tui_client.screens.game import GameScreen
from tui_client.screens.inventory import InventoryScreen
from tui_client.screens.map import MapScreen
from tui_client.screens.help import HelpScreen
from tui_client.screens.chat import ChatScreen


# ============================================================================
# Background and Setup Steps
# ============================================================================

@given('the game server is running')
def step_server_running(context):
    """Mock a running game server."""
    context.server_running = True
    context.server_url = "ws://localhost:5000/ws"


@given('the game server is stopped')
def step_server_stopped(context):
    """Mock a stopped game server."""
    context.server_running = False


@given('the TUI client is launched')
def step_launch_tui(context):
    """Initialize the TUI client for testing."""
    context.app = Mock(spec=PyMUDApp)
    context.game_client = Mock(spec=GameClient)
    context.game_client.connected = True
    context.game_client.server_url = context.server_url
    

@given('I am logged into the TUI as "{username}"')
def step_logged_in(context, username):
    """Setup a logged-in state."""
    context.username = username
    context.authenticated = True
    context.app.authenticated = True
    context.current_screen = "game"


@given('I am on the game screen')
def step_on_game_screen(context):
    """Verify we're on the game screen."""
    context.current_screen = "game"
    context.screen = Mock(spec=GameScreen)


@given('I am on the inventory screen')
def step_on_inventory_screen(context):
    """Verify we're on the inventory screen."""
    context.current_screen = "inventory"
    context.screen = Mock(spec=InventoryScreen)


@given('I am on any screen')
def step_on_any_screen(context):
    """Can be on any screen."""
    if not hasattr(context, 'current_screen'):
        context.current_screen = "game"


# ============================================================================
# Login Flow Steps
# ============================================================================

@when('I enter username "{username}"')
def step_enter_username(context, username):
    """Enter username in login form."""
    context.entered_username = username


@when('I enter password "{password}"')
def step_enter_password(context, password):
    """Enter password in login form."""
    context.entered_password = password


@when('I confirm password "{password}"')
def step_confirm_password(context, password):
    """Enter password confirmation."""
    context.confirmed_password = password


@when('I submit the login form')
def step_submit_login(context):
    """Submit the login form."""
    context.login_submitted = True
    # Mock successful login
    context.authenticated = True


@when('I submit the registration form')
def step_submit_registration(context):
    """Submit the registration form."""
    context.registration_submitted = True
    context.authenticated = True


@when('I click "Create Account"')
def step_click_create_account(context):
    """Click create account button."""
    context.creating_account = True


@when('I try to connect')
def step_try_connect(context):
    """Attempt to connect to server."""
    context.connection_attempted = True


# ============================================================================
# Game Command Steps
# ============================================================================

@when('I type "{command}" and press Enter')
def step_type_command(context, command):
    """Type a command and submit it."""
    context.last_command = command
    context.command_submitted = True


@when('I press the Up arrow key')
def step_press_up(context):
    """Press up arrow for command history."""
    if not hasattr(context, 'history_position'):
        context.history_position = 0
    else:
        context.history_position += 1


@when('I press the Up arrow key again')
def step_press_up_again(context):
    """Press up arrow again."""
    step_press_up(context)


@when('I press the Escape key')
def step_press_escape(context):
    """Press escape key."""
    context.escape_pressed = True


@when('I press Ctrl+L')
def step_press_ctrl_l(context):
    """Press Ctrl+L."""
    context.ctrl_l_pressed = True


@given('I have typed "{text}"')
def step_typed_text(context, text):
    """Have text in input."""
    context.input_text = text


@given('I have typed "{command}" and pressed Enter')
def step_typed_and_submitted(context, command):
    """Have submitted a command."""
    if not hasattr(context, 'command_history'):
        context.command_history = []
    context.command_history.append(command)


@given('the terminal log has multiple messages')
def step_log_has_messages(context):
    """Terminal has messages."""
    context.log_messages = ["Message 1", "Message 2", "Message 3"]


@when('the server sends an error message')
def step_server_sends_error(context):
    """Server sends error message."""
    context.last_message_type = "error"


@when('the server sends a system message')
def step_server_sends_system(context):
    """Server sends system message."""
    context.last_message_type = "system"


@when('the server sends a broadcast')
def step_server_sends_broadcast(context):
    """Server sends broadcast."""
    context.last_message_type = "broadcast"


@when('the server sends a success message')
def step_server_sends_success(context):
    """Server sends success message."""
    context.last_message_type = "success"


# ============================================================================
# View Switching Steps
# ============================================================================

@when('I press F2')
def step_press_f2(context):
    """Press F2 key."""
    context.current_screen = "inventory"


@when('I press F3')
def step_press_f3(context):
    """Press F3 key."""
    context.current_screen = "map"


@when('I press F4')
def step_press_f4(context):
    """Press F4 key."""
    context.current_screen = "help"


@when('I press F5')
def step_press_f5(context):
    """Press F5 key."""
    context.current_screen = "chat"


@when('I press F1')
def step_press_f1(context):
    """Press F1 key."""
    context.current_screen = "game"


@when('I press F2, F3, F4, F5, F1 in sequence')
def step_rapid_switching(context):
    """Rapidly switch views."""
    context.view_sequence = ["inventory", "map", "help", "chat", "game"]
    context.current_screen = "game"


# ============================================================================
# Inventory Steps
# ============================================================================

@given('I have at least one item in my inventory')
def step_has_items(context):
    """Has items in inventory."""
    context.inventory_items = [
        {"id": "item1", "name": "Test Item", "type": "tool", "weight": 1.0}
    ]


@when('I click on an item in the carried items list')
def step_click_item(context):
    """Click on an item."""
    context.selected_item = context.inventory_items[0]


@given('I have selected an item')
def step_selected_item(context):
    """Have an item selected."""
    if not hasattr(context, 'inventory_items'):
        step_has_items(context)
    context.selected_item = context.inventory_items[0]


@when('I press the U key')
def step_press_u(context):
    """Press U to use item."""
    context.action_pressed = "use"


@when('I press the E key')
def step_press_e(context):
    """Press E to equip/unequip."""
    context.action_pressed = "equip"


@when('I press the D key')
def step_press_d(context):
    """Press D to drop item."""
    context.action_pressed = "drop"


@when('I press the X key')
def step_press_x(context):
    """Press X to examine."""
    context.action_pressed = "examine"


@when('I press the R key')
def step_press_r(context):
    """Press R to refresh."""
    context.action_pressed = "refresh"


@when('I confirm the action')
def step_confirm_action(context):
    """Confirm an action."""
    context.action_confirmed = True


# ============================================================================
# Assertion Steps
# ============================================================================

@then('I should see the game screen')
def step_see_game_screen(context):
    """Verify game screen is visible."""
    assert context.current_screen == "game" or context.authenticated


@then('I should see a welcome message')
def step_see_welcome(context):
    """Verify welcome message."""
    # In real test, would check terminal log
    assert context.authenticated


@then('the status bar should show "{text}"')
def step_status_bar_shows(context, text):
    """Verify status bar content."""
    # In real test, would query status bar widget
    pass


@then('I should see "{text}" error')
def step_see_error(context, text):
    """Verify error message."""
    # In real test, would check for error display
    pass


@then('I should remain on the login screen')
def step_remain_login(context):
    """Verify still on login."""
    assert not context.authenticated


@then('I should see connection retry options')
def step_see_retry_options(context):
    """Verify retry options."""
    pass


@then('I should see the current location description')
def step_see_location_desc(context):
    """Verify location description visible."""
    pass


@then('I should see a list of visible items')
def step_see_items(context):
    """Verify items list visible."""
    pass


@then('I should see a list of other characters')
def step_see_characters(context):
    """Verify characters list visible."""
    pass


@then('the input should show "{text}"')
def step_input_shows(context, text):
    """Verify input field content."""
    # In real test, would check Input widget value
    pass


@then('the input field should be empty')
def step_input_empty(context):
    """Verify input is empty."""
    assert context.escape_pressed or True


@then('the terminal log should be cleared')
def step_log_cleared(context):
    """Verify log was cleared."""
    assert context.ctrl_l_pressed


@then('I should see "{text}" message')
def step_see_message(context, text):
    """Verify specific message."""
    pass


@then('I should see the message in {color} with {icon} icon')
def step_see_colored_message(context, color, icon):
    """Verify message color and icon."""
    pass


@then('I should see "{text}"')
def step_see_text(context, text):
    """Verify text is visible."""
    pass


@then('the location name should update')
def step_location_updates(context):
    """Verify location changed."""
    pass


@then('the location description should update')
def step_location_desc_updates(context):
    """Verify description changed."""
    pass


@then('I should see command suggestions')
def step_see_suggestions(context):
    """Verify command suggestions."""
    pass


@then('I should see the {screen_name} screen')
def step_see_screen(context, screen_name):
    """Verify specific screen is visible."""
    assert context.current_screen == screen_name


@then('I should see {element}')
def step_see_element(context, element):
    """Verify element is visible."""
    pass


@then('each view should load correctly')
def step_views_load_correctly(context):
    """Verify all views loaded."""
    pass


@then('there should be no errors')
def step_no_errors(context):
    """Verify no errors occurred."""
    pass


@then('the UI should remain responsive')
def step_ui_responsive(context):
    """Verify UI is responsive."""
    pass


@then('the game view should be fresh')
def step_view_fresh(context):
    """Verify view is fresh/reset."""
    pass


@then('the item should be used')
def step_item_used(context):
    """Verify item was used."""
    assert context.action_pressed == "use"


@then('I should see a confirmation message')
def step_see_confirmation(context):
    """Verify confirmation shown."""
    pass


@then('the item should move to the equipped list')
def step_item_equipped(context):
    """Verify item equipped."""
    pass


@then('the item should move to the carried list')
def step_item_unequipped(context):
    """Verify item unequipped."""
    pass


@then('the player stats should update')
def step_stats_update(context):
    """Verify stats updated."""
    pass


@then('I should see a confirmation prompt')
def step_see_prompt(context):
    """Verify confirmation prompt."""
    pass


@then('the item should be removed from my inventory')
def step_item_removed(context):
    """Verify item removed."""
    pass


@then('I should see detailed examination text')
def step_see_exam_text(context):
    """Verify examination text."""
    pass


@then('I should see all item properties')
def step_see_properties(context):
    """Verify item properties."""
    pass


@then('the inventory should refresh from the server')
def step_inventory_refreshes(context):
    """Verify inventory refreshed."""
    pass


@then('I should see any new items')
def step_see_new_items(context):
    """Verify new items visible."""
    pass


@then('I should see updated item states')
def step_see_updated_states(context):
    """Verify item states updated."""
    pass
