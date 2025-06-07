# MUDpy with WebSocket Interface

This project extends the MUDpy game engine with a WebSocket interface. Players can connect via a modern web browser instead of a Telnet client.

## Features

- **MUDpy Integration**: Interfaces with the MUDpy game engine.
- **Persistent Storage**: Uses YAML for configuration and data files.
- **Web-Based Frontend**: Connect through a browser using WebSockets.
- **NPC Data**: Non-player characters defined in `data/npcs.yaml`.
- **Command History and Dark Mode** support.
- **Responsive Design** for desktop and mobile.

## Requirements

- Python 3.6+
- Git
- WebSockets library for Python
- MUDpy

## Setup

Run the setup script to clone MUDpy and install dependencies:

```bash
chmod +x setup.sh
./setup.sh
```

Then start the combined HTTP/WebSocket server:

```bash
python run_server.py
```

The web client will be available on `http://localhost:5000`.

## License

This project is released under the [MIT License](LICENSE).
