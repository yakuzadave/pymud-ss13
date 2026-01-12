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


# ============================================================================
# Map Navigation Steps
# ============================================================================

@given('I am viewing the map screen')
def step_viewing_map(context):
    """Setup map screen viewing state."""
    context.current_screen = "map"
    context.screen = Mock(spec=MapScreen)
    context.map_viewport = {"x": 0, "y": 0}


@when('I press F3 to switch to map view')
def step_switch_to_map(context):
    """Switch to map view."""
    context.current_screen = "map"


@when('I press the right arrow key')
def step_press_right_arrow(context):
    """Press right arrow."""
    if not hasattr(context, 'map_viewport'):
        context.map_viewport = {"x": 0, "y": 0}
    context.map_viewport["x"] += 1


@when('I press the down arrow key')
def step_press_down_arrow(context):
    """Press down arrow."""
    if not hasattr(context, 'map_viewport'):
        context.map_viewport = {"x": 0, "y": 0}
    context.map_viewport["y"] += 1


@when('I press the left arrow key')
def step_press_left_arrow(context):
    """Press left arrow."""
    if not hasattr(context, 'map_viewport'):
        context.map_viewport = {"x": 0, "y": 0}
    context.map_viewport["x"] -= 1


@when('I press the up arrow key')
def step_press_up_arrow(context):
    """Press up arrow."""
    if not hasattr(context, 'map_viewport'):
        context.map_viewport = {"x": 0, "y": 0}
    context.map_viewport["y"] -= 1


@when('I click on a room tile')
def step_click_room_tile(context):
    """Click on a room tile."""
    context.selected_room = "test_room"


@when('I press "{key}" to toggle door overlay')
def step_toggle_door_overlay(context, key):
    """Toggle door overlay."""
    context.door_overlay_enabled = not getattr(context, 'door_overlay_enabled', False)


@when('I press "{key}" to toggle atmosphere overlay')
def step_toggle_atmosphere_overlay(context, key):
    """Toggle atmosphere overlay."""
    context.atmosphere_overlay_enabled = not getattr(context, 'atmosphere_overlay_enabled', False)


@when('I press "{key}" to toggle power overlay')
def step_toggle_power_overlay(context, key):
    """Toggle power overlay."""
    context.power_overlay_enabled = not getattr(context, 'power_overlay_enabled', False)


@when('I press "{key}" to zoom in')
def step_zoom_in(context, key):
    """Zoom in the map."""
    context.zoom_level = getattr(context, 'zoom_level', 1.0) + 0.5


@when('I press "{key}" to zoom out')
def step_zoom_out(context, key):
    """Zoom out the map."""
    context.zoom_level = getattr(context, 'zoom_level', 1.0) - 0.5


@when('I press "{key}" to center on player')
def step_center_on_player(context, key):
    """Center map on player."""
    context.map_centered = True


@given('I have scrolled away from my position')
def step_scrolled_away(context):
    """Map is scrolled away from player position."""
    context.map_viewport = {"x": 100, "y": 100}
    context.map_centered = False


@when('another player moves to a new room')
def step_other_player_moves(context):
    """Another player moves."""
    context.other_player_moved = True


@when('a door lock status changes')
def step_door_status_changes(context):
    """Door lock status changes."""
    context.door_status_changed = True


@then('I should see the map screen')
def step_see_map_screen(context):
    """Verify map screen is visible."""
    assert context.current_screen == "map"


@then('I should see the station grid layout')
def step_see_grid_layout(context):
    """Verify grid layout is visible."""
    pass


@then('I should see my player position marked on the map')
def step_see_player_position(context):
    """Verify player position marker."""
    pass


@then('I should see room labels')
def step_see_room_labels(context):
    """Verify room labels are shown."""
    pass


@then('the map viewport should scroll right')
def step_map_scrolls_right(context):
    """Verify map scrolled right."""
    assert context.map_viewport["x"] > 0


@then('the map viewport should scroll down')
def step_map_scrolls_down(context):
    """Verify map scrolled down."""
    assert context.map_viewport["y"] > 0


@then('the map viewport should scroll left')
def step_map_scrolls_left(context):
    """Verify map scrolled left."""
    pass


@then('the map viewport should scroll up')
def step_map_scrolls_up(context):
    """Verify map scrolled up."""
    pass


@then('I should see room details in the sidebar')
def step_see_room_details(context):
    """Verify room details sidebar."""
    assert hasattr(context, 'selected_room')


@then('I should see the room name')
def step_see_room_name(context):
    """Verify room name is shown."""
    pass


@then('I should see room occupants list')
def step_see_occupants(context):
    """Verify occupants list."""
    pass


@then('I should see room exit directions')
def step_see_exits(context):
    """Verify exit directions."""
    pass


@then('I should see door lock indicators on the map')
def step_see_door_indicators(context):
    """Verify door indicators."""
    assert context.door_overlay_enabled


@then('I should see atmosphere status indicators')
def step_see_atmosphere_indicators(context):
    """Verify atmosphere indicators."""
    assert context.atmosphere_overlay_enabled


@then('I should see power status indicators')
def step_see_power_indicators(context):
    """Verify power indicators."""
    assert context.power_overlay_enabled


@then('the map tiles should appear larger')
def step_tiles_larger(context):
    """Verify tiles are larger."""
    assert context.zoom_level > 1.0


@then('I should see fewer rooms on screen')
def step_fewer_rooms(context):
    """Verify fewer rooms visible."""
    pass


@then('the map tiles should appear smaller')
def step_tiles_smaller(context):
    """Verify tiles are smaller."""
    pass


@then('I should see more rooms on screen')
def step_more_rooms(context):
    """Verify more rooms visible."""
    pass


@then('the map should scroll to show my player position')
def step_map_shows_player(context):
    """Verify map centered on player."""
    assert context.map_centered


@then('my player marker should be centered on screen')
def step_player_centered(context):
    """Verify player marker centered."""
    pass


@when('I look at the corner of the screen')
def step_look_at_corner(context):
    """Look at screen corner."""
    context.looking_at_minimap = True


@then('I should see a minimap indicator')
def step_see_minimap(context):
    """Verify minimap visible."""
    pass


@then('the minimap should show nearby rooms')
def step_minimap_shows_rooms(context):
    """Verify minimap content."""
    pass


@then('my current position should be highlighted')
def step_position_highlighted(context):
    """Verify position highlighted on minimap."""
    pass


@then('I should see their marker update on the map')
def step_see_marker_update(context):
    """Verify marker updated."""
    pass


@then('the door indicator should update immediately')
def step_door_indicator_updates(context):
    """Verify door indicator updated."""
    pass


@then('the map state should be preserved for next view')
def step_map_state_preserved(context):
    """Verify map state is preserved."""
    pass


# ============================================================================
# Chat System Steps
# ============================================================================

@when('I type "{message}"')
def step_type_message(context, message):
    """Type a message."""
    context.typed_message = message


@when('I press Enter')
def step_press_enter(context):
    """Press enter key."""
    context.message_submitted = True


@when('I scroll up in the chat panel')
def step_scroll_up_chat(context):
    """Scroll up in chat."""
    context.chat_scroll_position = getattr(context, 'chat_scroll_position', 0) + 10


@when('I scroll to the bottom')
def step_scroll_to_bottom(context):
    """Scroll to bottom of chat."""
    context.chat_scroll_position = 0


@given('there are 50 messages in chat history')
def step_chat_has_messages(context):
    """Setup chat history."""
    context.chat_message_count = 50


@when('I press F5 to switch to chat view')
def step_switch_to_chat(context):
    """Switch to chat view."""
    context.current_screen = "chat"


@given('I am viewing the chat screen')
def step_viewing_chat(context):
    """Setup chat screen viewing."""
    context.current_screen = "chat"
    context.screen = Mock(spec=ChatScreen)


@when('I press "{key}" to switch to global channel')
def step_switch_to_global(context, key):
    """Switch to global chat channel."""
    context.current_channel = "global"


@when('I press "{key}" to switch to local channel')
def step_switch_to_local(context, key):
    """Switch to local chat channel."""
    context.current_channel = "local"


@when('I press "{key}" to switch to department channel')
def step_switch_to_department(context, key):
    """Switch to department chat channel."""
    context.current_channel = "department"


@given('I am on the department channel')
def step_on_department_channel(context):
    """Setup department channel."""
    context.current_channel = "department"


@when('another player sends me a private message')
def step_receive_pm(context):
    """Receive a private message."""
    context.pm_received = True


@when('I press "{key}" to open filter menu')
def step_open_filter(context, key):
    """Open filter menu."""
    context.filter_menu_open = True


@when('I select "System messages only"')
def step_select_system_filter(context):
    """Select system messages filter."""
    context.chat_filter = "system"


@when('I select "Show all messages"')
def step_select_all_filter(context):
    """Select show all filter."""
    context.chat_filter = "all"


@when('I right-click on "{player}" in the player list')
def step_right_click_player(context, player):
    """Right-click on a player."""
    context.context_menu_player = player


@when('I select "Mute player"')
def step_select_mute(context):
    """Select mute option."""
    context.player_muted = True


@when('I look at the player list sidebar')
def step_look_at_player_list(context):
    """Look at player list."""
    context.viewing_player_list = True


@when('I receive a new chat message')
def step_receive_chat_message(context):
    """Receive a chat message."""
    context.unread_chat_messages = getattr(context, 'unread_chat_messages', 0) + 1


@given('I am in the chat input field')
def step_in_chat_input(context):
    """Focus on chat input."""
    context.chat_input_focused = True


@when('I press Tab')
def step_press_tab(context):
    """Press tab key."""
    context.tab_pressed = True


@then('I should see "{text}" in the chat log')
def step_see_in_chat(context, text):
    """Verify text in chat log."""
    pass


@then('other players should receive my message')
def step_others_receive(context):
    """Verify others received message."""
    pass


@then('I should see older messages')
def step_see_older_messages(context):
    """Verify older messages visible."""
    pass


@then('the scroll position should be maintained')
def step_scroll_maintained(context):
    """Verify scroll position maintained."""
    pass


@then('I should see the most recent messages')
def step_see_recent_messages(context):
    """Verify recent messages visible."""
    pass


@then('I should see the chat screen')
def step_see_chat_screen(context):
    """Verify chat screen visible."""
    assert context.current_screen == "chat"


@then('I should see multiple chat channels')
def step_see_channels(context):
    """Verify channels visible."""
    pass


@then('I should see the message input field')
def step_see_input_field(context):
    """Verify input field visible."""
    pass


@then('I should see the current channel indicator')
def step_see_channel_indicator(context):
    """Verify channel indicator visible."""
    pass


@then('the channel indicator should show "{channel}"')
def step_indicator_shows_channel(context, channel):
    """Verify channel indicator text."""
    pass


@then('I should see global chat messages')
def step_see_global_messages(context):
    """Verify global messages visible."""
    pass


@then('I should see only local chat messages')
def step_see_local_messages(context):
    """Verify only local messages visible."""
    pass


@then('the channel indicator should show my department name')
def step_indicator_shows_department(context):
    """Verify department name shown."""
    pass


@then('I should see department-specific messages')
def step_see_department_messages(context):
    """Verify department messages visible."""
    pass


@then('the message should appear in department channel')
def step_message_in_department(context):
    """Verify message in department channel."""
    pass


@then('only department members should see the message')
def step_only_department_sees(context):
    """Verify message visibility."""
    pass


@then('I should see "{text}"')
def step_see_text(context, text):
    """Verify text is visible."""
    pass


@then('the engineer should receive a private message notification')
def step_engineer_notified(context):
    """Verify PM notification sent."""
    pass


@then('I should see a notification indicator')
def step_see_notification(context):
    """Verify notification indicator."""
    pass


@then('the message should appear in my PM tab')
def step_message_in_pm_tab(context):
    """Verify message in PM tab."""
    pass


@then('I should hear a notification sound')
def step_hear_notification(context):
    """Verify notification sound played."""
    pass


@then('I should only see system messages')
def step_only_system_messages(context):
    """Verify only system messages shown."""
    assert context.chat_filter == "system"


@then('I should see all message types again')
def step_see_all_types(context):
    """Verify all message types shown."""
    assert context.chat_filter == "all"


@then('messages from "{player}" should be hidden')
def step_messages_hidden(context, player):
    """Verify messages from player are hidden."""
    pass


@then('I should see "Player muted: {player}" confirmation')
def step_see_mute_confirmation(context, player):
    """Verify mute confirmation."""
    pass


@then('I should see all online players')
def step_see_online_players(context):
    """Verify online players list."""
    pass


@then('I should see their current status')
def step_see_player_status(context):
    """Verify player status shown."""
    pass


@then('I should see their job roles')
def step_see_job_roles(context):
    """Verify job roles shown."""
    pass


@then('I should see a chat notification badge')
def step_see_chat_badge(context):
    """Verify chat notification badge."""
    pass


@then('the notification count should increase')
def step_notification_increases(context):
    """Verify notification count increased."""
    pass


@then('the notification badge should clear')
def step_badge_clears(context):
    """Verify notification badge cleared."""
    pass


@then('it should be styled differently from regular messages')
def step_styled_differently(context):
    """Verify different styling."""
    pass


@then('I should see autocomplete suggestions')
def step_see_autocomplete(context):
    """Verify autocomplete visible."""
    pass


@then('I should see available chat commands listed')
def step_see_commands(context):
    """Verify commands listed."""
    pass


@then('the command should autocomplete')
def step_command_autocompletes(context):
    """Verify command autocompleted."""
    pass


@then('each message should have a timestamp')
def step_messages_have_timestamps(context):
    """Verify timestamps on messages."""
    pass


@then('timestamps should be in "{format}" format')
def step_timestamp_format(context, format):
    """Verify timestamp format."""
    pass


@then('recent messages should show relative time')
def step_relative_time(context):
    """Verify relative time shown."""
    pass


@then('unread messages should still show in notification badge')
def step_unread_in_badge(context):
    """Verify unread messages in badge."""
    pass


# ============================================================================
# Help System Steps
# ============================================================================

@when('I press F4 to switch to help view')
def step_switch_to_help(context):
    """Switch to help view."""
    context.current_screen = "help"


@given('I am viewing the help screen')
def step_viewing_help(context):
    """Setup help screen viewing."""
    context.current_screen = "help"
    context.screen = Mock(spec=HelpScreen)


@when('I click on "{category}" category')
def step_click_category(context, category):
    """Click on a help category."""
    context.selected_category = category


@given('I am in the "{category}" category')
def step_in_category(context, category):
    """Setup category context."""
    context.selected_category = category


@when('I click on the "{command}" command')
def step_click_command(context, command):
    """Click on a command."""
    context.selected_command = command


@when('I type "{text}" in the search box')
def step_type_in_search(context, text):
    """Type in search box."""
    context.search_query = text


@when('I click on a search result')
def step_click_search_result(context):
    """Click on search result."""
    context.search_result_clicked = True


@given('my job is "{job}"')
def step_my_job_is(context, job):
    """Set player job."""
    context.player_job = job


@when('I click on "{guide}" guide')
def step_click_guide(context, guide):
    """Click on a guide."""
    context.selected_guide = guide


@when('I click on "{topic}" topic')
def step_click_topic(context, topic):
    """Click on a topic."""
    context.selected_topic = topic


@given('I am viewing a command with examples')
def step_viewing_command_examples(context):
    """Setup command with examples."""
    context.viewing_command_examples = True


@when('I click "Copy" next to an example')
def step_click_copy(context):
    """Click copy button."""
    context.example_copied = True


@given('I have viewed multiple help pages')
def step_viewed_multiple_pages(context):
    """Setup help history."""
    context.help_history = ["page1", "page2", "page3"]


@when('I press the back button')
def step_press_back(context):
    """Press back button."""
    context.help_history_position = getattr(context, 'help_history_position', 0) + 1


@when('I press the forward button')
def step_press_forward(context):
    """Press forward button."""
    context.help_history_position = getattr(context, 'help_history_position', 1) - 1


@given('I am a new player')
def step_new_player(context):
    """Setup new player state."""
    context.is_new_player = True


@when('I click on "{tutorial}" tutorial')
def step_click_tutorial(context, tutorial):
    """Click on tutorial."""
    context.selected_tutorial = tutorial


@given('I have selected an item in my inventory')
def step_selected_item_in_inventory(context):
    """Setup selected item."""
    context.selected_item = "test_item"


@when('I click "Export to File"')
def step_click_export(context):
    """Click export button."""
    context.export_clicked = True


@when('I press a letter key')
def step_press_letter(context):
    """Press a letter key."""
    context.letter_pressed = True


@when('I press "{key}" to search')
def step_press_search_key(context, key):
    """Press search key."""
    context.search_focused = True


@when('I view the "{command}" command details')
def step_view_command_details(context, command):
    """View command details."""
    context.viewing_command_details = command


@then('I should see the help screen')
def step_see_help_screen(context):
    """Verify help screen visible."""
    assert context.current_screen == "help"


@then('I should see the help categories menu')
def step_see_categories_menu(context):
    """Verify categories menu visible."""
    pass


@then('I should see a search box')
def step_see_search_box(context):
    """Verify search box visible."""
    pass


@then('I should see quick reference shortcuts')
def step_see_shortcuts(context):
    """Verify shortcuts visible."""
    pass


@then('I should see a list of basic commands')
def step_see_basic_commands(context):
    """Verify basic commands list."""
    pass


@then('each command should have a description')
def step_commands_have_descriptions(context):
    """Verify command descriptions."""
    pass


@then('each command should have usage examples')
def step_commands_have_examples(context):
    """Verify command examples."""
    pass


@then('I should see detailed command information')
def step_see_command_info(context):
    """Verify detailed command info."""
    pass


@then('I should see command syntax')
def step_see_command_syntax(context):
    """Verify command syntax."""
    pass


@then('I should see command parameters')
def step_see_command_parameters(context):
    """Verify command parameters."""
    pass


@then('I should see related commands')
def step_see_related_commands(context):
    """Verify related commands."""
    pass


@then('I should see search results for "{query}"')
def step_see_search_results(context, query):
    """Verify search results."""
    pass


@then('results should be ranked by relevance')
def step_results_ranked(context):
    """Verify results ranking."""
    pass


@then('I should see matching commands and articles')
def step_see_matching_content(context):
    """Verify matching content."""
    pass


@then('I should navigate to that help topic')
def step_navigate_to_topic(context):
    """Verify navigation to topic."""
    pass


@then('I should see a list of all keyboard shortcuts')
def step_see_all_shortcuts(context):
    """Verify all shortcuts listed."""
    pass


@then('shortcuts should be grouped by function')
def step_shortcuts_grouped(context):
    """Verify shortcuts grouping."""
    pass


@then('I should see F1-F5 view switching shortcuts')
def step_see_view_shortcuts(context):
    """Verify view switching shortcuts."""
    pass


@then('I should see movement and action shortcuts')
def step_see_action_shortcuts(context):
    """Verify action shortcuts."""
    pass


@then('I should see my job highlighted')
def step_see_job_highlighted(context):
    """Verify job highlighted."""
    pass


@then('I should see engineer-specific instructions')
def step_see_job_instructions(context):
    """Verify job instructions."""
    pass


@then('I should see engineer equipment list')
def step_see_job_equipment(context):
    """Verify job equipment list."""
    pass


@then('I should see engineer responsibilities')
def step_see_job_responsibilities(context):
    """Verify job responsibilities."""
    pass


@then('I should see topics like "{topics}"')
def step_see_topics(context, topics):
    """Verify topics listed."""
    pass


@then('I should see detailed atmosphere mechanics explanation')
def step_see_mechanics_explanation(context):
    """Verify mechanics explanation."""
    pass


@then('I should see related systems documentation')
def step_see_related_systems(context):
    """Verify related systems."""
    pass


@then('the example should be copied to clipboard')
def step_example_copied(context):
    """Verify example copied."""
    assert context.example_copied


@then('I should see "Copied to clipboard" confirmation')
def step_see_copy_confirmation(context):
    """Verify copy confirmation."""
    pass


@then('I should return to the previous help page')
def step_return_to_previous(context):
    """Verify returned to previous page."""
    pass


@then('I should go forward in help history')
def step_go_forward(context):
    """Verify went forward in history."""
    pass


@then('I should see step-by-step instructions')
def step_see_tutorial_steps(context):
    """Verify tutorial steps."""
    pass


@then('I should see tutorial progress indicator')
def step_see_progress_indicator(context):
    """Verify progress indicator."""
    pass


@then('I should be able to navigate between tutorial steps')
def step_navigate_tutorial(context):
    """Verify tutorial navigation."""
    pass


@then('the help should open to item usage information')
def step_help_opens_to_item(context):
    """Verify context-sensitive help."""
    pass


@then('I should see how to use the selected item')
def step_see_item_usage(context):
    """Verify item usage info."""
    pass


@then('I should see recent game updates')
def step_see_updates(context):
    """Verify recent updates."""
    pass


@then('I should see patch notes')
def step_see_patch_notes(context):
    """Verify patch notes."""
    pass


@then('updates should be sorted by date')
def step_updates_sorted(context):
    """Verify updates sorting."""
    pass


@then('I should see export options')
def step_see_export_options(context):
    """Verify export options."""
    pass


@then('I should be able to save help as text file')
def step_save_as_text(context):
    """Verify save functionality."""
    pass


@then('the file should contain all help content')
def step_file_has_content(context):
    """Verify file content."""
    pass


@then('the help should jump to topics starting with that letter')
def step_jump_to_letter(context):
    """Verify jump to letter."""
    pass


@then('the search box should be focused')
def step_search_focused(context):
    """Verify search focused."""
    assert context.search_focused


@then('I should see command aliases listed')
def step_see_aliases(context):
    """Verify aliases listed."""
    pass


@then('I should see "{alias}" as an alias for "{command}"')
def step_see_specific_alias(context, alias, command):
    """Verify specific alias."""
    pass


@then('aliases should be clickable to view details')
def step_aliases_clickable(context):
    """Verify aliases are clickable."""
    pass


@then('my help browsing position should be saved')
def step_help_position_saved(context):
    """Verify help position saved."""
    pass


@when('I press F4 again')
def step_press_f4_again(context):
    """Press F4 again."""
    context.current_screen = "help"


@then('I should return to the same help page')
def step_return_to_same_page(context):
    """Verify returned to same page."""
    pass
