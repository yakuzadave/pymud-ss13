# PyMUD-SS13 Textual TUI Client

A full-featured Terminal User Interface for PyMUD-SS13, built with the [Textual](https://textual.textualize.io/) framework.

## Features

### 🎮 Multiple Views

Switch seamlessly between different views using function keys:

- **F1 - Game View**: Main gameplay interface with terminal output and command input
- **F2 - Inventory View**: Comprehensive item and equipment management
- **F3 - Map View**: Visual grid-based station map with real-time updates
- **F4 - Help View**: Complete command reference and keybindings
- **F5 - Chat View**: Dedicated communication interface with multiple channels
- **F10 - Quit**: Exit the application

### 🖥️ Game View (F1)

- Real-time terminal output with colored messages
- Command input with history (Up/Down arrows)
- Status bar showing location, health, and connection status
- Current location display with description
- Timestamped message log

### 🎒 Inventory View (F2)

- Separate lists for carried and equipped items
- Detailed item information panel
- One-click item actions (Use, Equip, Drop)
- Player stats display (weight, capacity, credits)
- Quick actions with keyboard shortcuts (U, E, D, X)

### 🗺️ Map View (F3)

- Visual grid-based map of the station
- Real-time player position tracking
- Color-coded room types and features
- Legend with symbol explanations
- Quick navigation with arrow keys
- Zoom controls (+ / -)

### ❓ Help View (F4)

- Tabbed interface with multiple sections
- Complete game command reference
- Keyboard shortcut guide
- Tips and tricks
- About information

### 💬 Chat View (F5)

- Multiple chat channels (Say, Yell, Whisper, Radio, OOC, System)
- Tabbed interface for organized conversations
- Online player list with roles
- Channel-specific color coding
- Quick channel switching with Tab/Shift+Tab
- Slash commands for advanced features
- Real-time message history
- Player count display

## Installation

The TUI client is included in the main PyMUD-SS13 installation. Make sure you have the required dependencies:

```bash
pip install textual websockets
```

## Usage

### Quick Start

Run the TUI client with default settings (localhost:5000):

```bash
python -m tui_client
```

### Custom Server

Connect to a specific server:

```bash
python -m tui_client --host 192.168.1.100 --port 5000
```

### Command Line Options

```
usage: python -m tui_client [-h] [--host HOST] [--port PORT] [--version]

Options:
  -h, --help     Show help message and exit
  --host HOST    Server host address (default: localhost)
  --port PORT    Server port number (default: 5000)
  --version      Show version number and exit
```

## Keyboard Shortcuts

### Global (All Views)

| Key | Action |
|-----|--------|
| F1 | Switch to Game view |
| F2 | Switch to Inventory view |
| F3 | Switch to Map view |
| F4 | Switch to Help view |
| F5 | Switch to Chat view |
| F10 | Quit application |
| Ctrl+C | Quit application |

### Game View

| Key | Action |
|-----|--------|
| Up/Down | Navigate command history |
| Escape | Clear command input |
| Ctrl+L | Clear terminal log |
| Enter | Submit command |

### Inventory View

| Key | Action |
|-----|--------|
| U | Use selected item |
| E | Equip/Unequip selected item |
| D | Drop selected item |
| X | Examine selected item |
| R | Refresh inventory |

### Map View

| Key | Action |
|-----|--------|
| Arrow Keys | Navigate in direction |
| + | Zoom in |
| - | Zoom out |
| R | Refresh map |

### Chat View

| Key | Action |
|-----|--------|
| Enter | Send message |
| Escape | Clear input |
| Tab | Next channel |
| Shift+Tab | Previous channel |
| Ctrl+L | Clear current channel |

#### Chat Slash Commands

| Command | Description |
|---------|-------------|
| /help | Show available commands |
| /say <msg> | Say something |
| /yell <msg> | Yell something |
| /whisper <player> <msg> | Whisper to someone |
| /radio <msg> | Send radio message |
| /ooc <msg> | Out of character chat |
| /who | List online players |
| /clear | Clear current channel |

## Architecture

### Directory Structure

```
tui_client/
├── __init__.py          # Package initialization
├── app.py               # Main application and screen management
├── app.tcss             # Global CSS styles
├── client.py            # WebSocket game client
├── README.md            # This file
└── screens/             # Screen implementations
    ├── __init__.py      # Screens package
    ├── login.py         # Login and authentication
    ├── game.py          # Main game interface
    ├── inventory.py     # Inventory management
    ├── map.py           # Map visualization
    ├── chat.py          # Chat and communication
    └── help.py          # Help and reference
```

### Key Components

#### PyMUDApp (app.py)

The main application class that manages screen switching and global state.

#### GameClient (client.py)

WebSocket client that handles all server communication with message routing to appropriate handlers.

#### Screen Classes

Each view is implemented as a Textual Screen with:
- Custom layout and widgets
- Event handlers for user interaction
- Message handlers for server updates
- Keyboard bindings for quick actions

## Customization

### Styling

Modify `tui_client/app.tcss` to customize colors, borders, and layout. Textual uses CSS-like syntax for styling.

### Adding New Views

1. Create a new screen in `tui_client/screens/`
2. Import in `tui_client/app.py`
3. Add binding in `PyMUDApp.BINDINGS`
4. Add switch case in `action_switch_screen()`

### Message Handlers

Register custom message handlers in any screen:

```python
def on_mount(self):
    self.game_client.register_handler("custom_type", self._handle_custom)

def _handle_custom(self, data: dict):
    # Handle custom message
    pass
```

## Tips & Tricks

- **Command History**: Use Up/Down arrows in the Game view to quickly access previous commands
- **Quick Navigation**: Use arrow keys in Map view for faster movement
- **Item Selection**: Click on items in Inventory view to see detailed information
- **Real-time Updates**: All views update automatically when server sends new data
- **Multiple Sessions**: You can run multiple TUI clients to different servers

## Troubleshooting

### Connection Issues

If you can't connect to the server:

1. Make sure the server is running (`python run_server.py`)
2. Check the host and port are correct
3. Verify firewall settings allow the connection

### Display Issues

If the interface looks wrong:

1. Make sure your terminal supports 256 colors
2. Try resizing the terminal window
3. Update to the latest version of Textual

### Performance

For best performance:

1. Use a modern terminal emulator (iTerm2, Windows Terminal, etc.)
2. Limit terminal log size with Ctrl+L in Game view
3. Close unused views

## Development

### Running in Development Mode

```bash
# With debug logging
textual run --dev tui_client/app.py

# With Textual console
textual console
textual run --dev tui_client/app.py
```

### Testing

```bash
# Run the client against a test server
python -m tui_client --host localhost --port 5000
```

## Credits

Built with:
- [Textual](https://textual.textualize.io/) - TUI framework by Textualize
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [websockets](https://websockets.readthedocs.io/) - WebSocket client library

## License

Part of the PyMUD-SS13 project.
