# MUDpy with WebSocket Interface

This project extends the MUDpy game engine with a WebSocket interface. Players can connect via a modern web browser instead of a Telnet client.

## Features

- **MUDpy Integration**: Interfaces with the MUDpy game engine.
- **Persistent Storage**: Uses YAML for configuration and data files.
- **Web-Based Frontend**: Connect through a browser using WebSockets.
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

## Command Line Interface

For quick local testing you can also use a simple CLI.

```bash
python cli.py
```

This launches a text prompt using the same engine as the server. Type commands
like `look`, `go north`, or `inventory`. Use `quit` to exit.

Additional project notes are available in `docs/development_plan.md` and
external references are listed in `docs/resources.md`.
