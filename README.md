# MUDpy with WebSocket Interface

This project extends the MUDpy game engine with a WebSocket interface, allowing players to connect through a web browser instead of requiring a Telnet client.

## Features

- **MUDpy Integration**: Seamlessly interfaces with the MUDpy game engine.
- **Persistent Storage**: Uses YAML files for configuration and data storage.
- **Web-Based Frontend**: Allows players to connect through a browser.
- **Real-Time Communication**: Uses WebSockets for bi-directional communication.
- **Command History**: Keeps track of command history for easy reuse.
- **Dark Mode**: Supports both light and dark themes.
- **Mobile Responsive**: Works on desktop and mobile devices.

## Requirements

- Python 3.6+
- Git
- WebSockets library for Python
- MUDpy

## Setup

1. Run the setup script to clone MUDpy and set up the environment:

```bash
chmod +x setup.sh
./setup.sh
