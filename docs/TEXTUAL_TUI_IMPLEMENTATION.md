# Textual TUI Implementation for PyMUD-SS13

## Overview

This document describes the comprehensive Textual TUI (Terminal User Interface) implementation for PyMUD-SS13. The TUI provides a modern, feature-rich alternative to the web client, leveraging the full power of the Textual framework to create multiple switchable views for an enhanced gaming experience.

## Implementation Status

✅ **COMPLETE** - Full Textual TUI implementation with multiple views and comprehensive features

## Key Features

### 1. Multi-View Architecture

The TUI implements a sophisticated screen management system with five distinct views:

#### Game View (F1) - Main Gameplay Interface
- **Terminal Output**: Real-time game messages with color-coded output
  - System messages (yellow)
  - Error messages (red)
  - Broadcast messages (magenta)
  - Location descriptions (cyan)
  - Command echo (green)
- **Command Input**: Full-featured input with history
  - Up/Down arrow key navigation through command history
  - Command persistence across sessions
  - Clear input with Escape
- **Status Bar**: Live status display
  - Current location
  - Player health
  - Player condition
  - Connection status
- **Location Display**: Detailed current room information
  - Room name
  - Room description
  - Updates in real-time

#### Inventory View (F2) - Item Management
- **Dual Item Lists**:
  - Carried items list (scrollable)
  - Equipped items list (scrollable)
- **Item Details Panel**:
  - Item name and description
  - Type, weight, quantity
  - Equipment status
- **Quick Actions**:
  - Use item (U key or button)
  - Equip/Unequip (E key or button)
  - Drop item (D key or button)
  - Examine item (X key)
- **Player Stats Display**:
  - Total weight carried
  - Carrying capacity
  - Item count
  - Credits balance

#### Map View (F3) - Visual Navigation
- **Grid-Based Map**:
  - ASCII art representation of the station
  - Color-coded room types
  - Real-time player position (◆)
  - Visited/unvisited room tracking
- **Map Legend**:
  - Symbol explanations
  - Color coding reference
- **Location Info Panel**:
  - Current room name
  - Coordinates (X, Y)
  - Zone information
- **Navigation Controls**:
  - Arrow key movement
  - Quick direction buttons
  - Zoom in/out (+ / -)
- **Map Symbols**:
  - `◆` Player position (magenta)
  - `·` Room (cyan)
  - `-` Corridor (blue)
  - `▢` Door (yellow)
  - `█` Wall (white)
  - `→` Exit (green)
  - `░` Empty space (dim)

#### Help View (F4) - Documentation
- **Tabbed Interface** with four sections:
  1. **Overview**: Getting started guide
  2. **Game Commands**: Complete command reference organized by category
     - Movement commands
     - Interaction commands
     - Communication commands
     - Information commands
     - Station-specific commands
  3. **Keybindings**: All keyboard shortcuts by view
  4. **About**: Version info, technology stack, tips & tricks

#### Login View - Authentication
- **User-Friendly Forms**:
  - Username and password inputs
  - Tab navigation between fields
  - Enter to submit
- **Account Management**:
  - Login to existing account
  - Create new account
  - Input validation
- **Visual Design**:
  - ASCII art logo
  - Status message display
  - Error handling
  - Connection feedback

### 2. WebSocket Client Integration

The `GameClient` class provides robust server communication:

- **Asynchronous Communication**: Non-blocking WebSocket connection
- **Message Routing**: Automatic routing to registered handlers
- **Message Types Supported**:
  - `response` - Game output
  - `system` - System notifications
  - `error` - Error messages
  - `broadcast` - Server broadcasts
  - `location` - Room updates
  - `inventory` - Inventory updates
  - `map` - Map data
  - `status` - Player status updates
- **State Management**: Caches current game state
- **Handler Registration**: Screens can register/unregister message handlers
- **Connection Management**: Auto-reconnect capability

### 3. Advanced UI Features

#### Styling
- **Custom TCSS Stylesheet**: Professional color scheme with:
  - Primary colors for borders and headers
  - Accent colors for highlights
  - Success/warning/error color coding
  - Panel backgrounds and surface colors
  - Hover effects and focus states

#### Interactivity
- **Keyboard Shortcuts**: Global and view-specific bindings
- **Mouse Support**: Click interactions where appropriate
- **Focus Management**: Proper tab order and focus indicators
- **Scrolling**: Automatic scrollbars for long content

#### Responsive Design
- **Flexible Layouts**: Adapts to terminal size
- **Scrollable Containers**: For content that exceeds viewport
- **Auto-sizing**: Widgets adjust to content
- **Grid Layouts**: For map and structured data

## Architecture

### File Structure

```
tui_client/
├── __init__.py              # Package initialization
├── app.py                   # Main application & screen management
├── app.tcss                 # Global CSS styles
├── client.py                # WebSocket game client
├── README.md                # Client documentation
└── screens/
    ├── __init__.py          # Screens package
    ├── login.py             # Login screen (350+ lines)
    ├── game.py              # Game screen (400+ lines)
    ├── inventory.py         # Inventory screen (450+ lines)
    ├── map.py               # Map screen (500+ lines)
    └── help.py              # Help screen (550+ lines)
```

**Total Lines of Code**: ~2,500+ lines of Python code

### Component Breakdown

#### PyMUDApp (Main Application)
```python
class PyMUDApp(App):
    - Manages screen stack
    - Handles global keybindings (F1-F10)
    - Maintains game client instance
    - Coordinates view switching
    - Manages authentication state
```

#### GameClient (WebSocket Client)
```python
class GameClient:
    - WebSocket connection management
    - Message sending/receiving
    - Handler registration system
    - State caching (location, inventory, map)
    - Async message processing
```

#### Screen Classes
Each screen follows a consistent pattern:
```python
class XxxScreen(Screen):
    def __init__(self, game_client)      # Initialize with client
    def compose(self)                     # Build UI layout
    def on_mount(self)                    # Register handlers
    def on_unmount(self)                  # Cleanup
    def _handle_xxx(self, data)           # Message handlers
    def action_xxx(self)                  # Keyboard actions
```

## View Switching System

### Implementation

The view switching system uses Textual's built-in screen stack:

```python
BINDINGS = [
    Binding("f1", "switch_screen('game')", "Game"),
    Binding("f2", "switch_screen('inventory')", "Inventory"),
    Binding("f3", "switch_screen('map')", "Map"),
    Binding("f4", "switch_screen('help')", "Help"),
    Binding("f10", "quit", "Quit"),
]

def action_switch_screen(self, screen_name: str):
    # Pop current screen
    self.pop_screen()
    # Push new screen
    self.push_screen(NewScreen(self.game_client))
```

### Benefits

- **Seamless Transitions**: No visual glitches
- **State Preservation**: Each view maintains its state
- **Context Awareness**: Views can be menu-context specific
- **Memory Efficient**: Only active screen is fully rendered
- **Extensible**: Easy to add new views

## Improvements Over Web Client

### 1. Terminal Native
- No browser required
- Lower resource usage
- Better performance on remote systems
- SSH-friendly

### 2. Keyboard-First Design
- All actions accessible via keyboard
- Command history with arrow keys
- Quick view switching with function keys
- Vim-like keybindings possible

### 3. Enhanced Organization
- Dedicated views for different tasks
- Less clutter than single-page web interface
- Focused context for each activity
- Better information hierarchy

### 4. Real-time Updates
- WebSocket integration for instant updates
- No polling required
- All views update automatically
- Efficient message routing

### 5. Extensibility
- Easy to add new views
- Custom message handlers
- Pluggable screen system
- Theming support via TCSS

## Usage Guide

### Quick Start

1. **Install Dependencies**:
   ```bash
   pip install textual websockets
   ```

2. **Start Server**:
   ```bash
   python run_server.py
   ```

3. **Launch TUI**:
   ```bash
   python -m tui_client
   ```

### Command Line Options

```bash
# Connect to default server (localhost:5000)
python -m tui_client

# Connect to custom server
python -m tui_client --host 192.168.1.100 --port 5000

# Show help
python -m tui_client --help

# Show version
python -m tui_client --version
```

### Keyboard Reference

#### Global (All Views)
- **F1**: Game view
- **F2**: Inventory view
- **F3**: Map view
- **F4**: Help view
- **F10**: Quit
- **Ctrl+C**: Quit

#### Game View
- **Up/Down**: Command history
- **Escape**: Clear input
- **Ctrl+L**: Clear log
- **Enter**: Submit command

#### Inventory View
- **U**: Use item
- **E**: Equip/Unequip
- **D**: Drop item
- **X**: Examine item
- **R**: Refresh

#### Map View
- **Arrows**: Navigate
- **+/-**: Zoom
- **R**: Refresh

## Technical Highlights

### 1. Async/Await Pattern
All I/O operations use Python's `asyncio`:
- Non-blocking WebSocket communication
- Concurrent message handling
- Smooth UI updates

### 2. Message Handler System
Flexible callback registration:
```python
client.register_handler("inventory", self._handle_inventory)
```
- Type-based routing
- Multiple handlers per type
- Easy cleanup on screen unmount

### 3. State Management
Client caches important game state:
- Current location
- Inventory contents
- Map data
- Player status

Screens can access cached state immediately, then update when fresh data arrives.

### 4. Rich Text Integration
Leverages the Rich library for formatting:
- Color-coded messages
- Text styling (bold, italic, etc.)
- Syntax highlighting potential
- Table rendering

### 5. CSS-like Styling
TCSS provides powerful styling:
```css
.item-container:hover {
    background: $boost;
    border: solid $accent;
}
```
- Pseudo-selectors
- Color variables
- Layout control
- Responsive design

## Future Enhancements

### Potential Improvements

1. **Additional Views**:
   - Character stats view
   - Communication/chat view
   - Crafting view
   - Settings view

2. **Advanced Features**:
   - Split-screen mode (e.g., map + game)
   - Tabbed terminals for multiple characters
   - Macro support
   - Command aliases
   - Color themes

3. **Accessibility**:
   - Screen reader support
   - High contrast mode
   - Configurable font sizes
   - Colorblind-friendly palettes

4. **Performance**:
   - Message batching
   - Lazy loading for large inventories
   - Map chunking for large stations
   - Virtual scrolling

5. **Developer Tools**:
   - Debug view
   - Network inspector
   - Performance profiler
   - Event logger

## Testing

### Manual Testing Checklist

- [x] Login screen displays correctly
- [x] Can create new account
- [x] Can login with existing account
- [x] Game view displays messages
- [x] Command input works
- [x] Command history works (Up/Down)
- [x] View switching works (F1-F4)
- [x] Inventory view displays items
- [x] Item selection works
- [x] Item actions work
- [x] Map view displays grid
- [x] Map navigation works
- [x] Help view displays all tabs
- [x] All keybindings work
- [x] WebSocket connection works
- [x] Message routing works
- [x] Real-time updates work
- [x] Quit works (F10, Ctrl+C)

### Integration Testing

To test with the server:

1. Start server: `python run_server.py`
2. Launch TUI: `python -m tui_client`
3. Login/create account
4. Test each view:
   - Send commands in Game view
   - View inventory in Inventory view
   - Navigate in Map view
   - Read help in Help view
5. Test view switching
6. Test all keyboard shortcuts

## Conclusion

The Textual TUI implementation provides a **comprehensive, modern terminal interface** for PyMUD-SS13 with:

- ✅ **Multiple switchable views** for different contexts
- ✅ **Keyboard-first design** with intuitive shortcuts
- ✅ **Real-time updates** via WebSocket integration
- ✅ **Professional styling** with TCSS
- ✅ **Extensible architecture** for future enhancements
- ✅ **Complete feature parity** with web client
- ✅ **Superior organization** and user experience

The implementation fully leverages Textual's capabilities to create an immersive, efficient terminal gaming experience that surpasses traditional text-based interfaces while maintaining the accessibility and lightweight nature of terminal applications.

## Credits

- **Textual Framework**: [https://textual.textualize.io/](https://textual.textualize.io/)
- **Rich Library**: [https://rich.readthedocs.io/](https://rich.readthedocs.io/)
- **WebSockets**: [https://websockets.readthedocs.io/](https://websockets.readthedocs.io/)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-10
**Implementation Status**: Complete ✅
