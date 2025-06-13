# MUDpy with WebSocket Interface

This project extends the MUDpy game engine with a WebSocket interface. Players can connect via a modern web browser instead of a Telnet client.

## Features

- **MUDpy Integration**: Interfaces with the MUDpy game engine.
- **Persistent Storage**: Uses YAML for configuration and data files.
- **Web-Based Frontend**: Connect through a browser using WebSockets.
- **NPC Data**: Non-player characters defined in `data/npcs.yaml`.
- **Command History and Dark Mode** support.
- **Responsive Design** for desktop and mobile.
- **Admin Event Control**: List and trigger random events using the `event` command.

## Requirements

- Python 3.6+
- Git
- WebSockets library for Python
- MUDpy

## Setup

Create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The repository also ships a helper script `setup.sh` which clones the `mudpy`
project and installs extra dependencies for the optional self‑test suite.

Start the combined HTTP/WebSocket server:

```bash
python run_server.py
```

The web client will be available on `http://localhost:5000`.


## Running Tests

Install pytest and run tests using:

```bash
pytest
```


## Random Events

Random station events are defined in `data/random_events.yaml`.  Each entry in
that file specifies an event name, its weight, and optional conditions for it to
occur.  The server loads these definitions at startup and the event manager
periodically picks one based on their weights, automatically running the
corresponding logic.

Administrators can fire an event with `event trigger <event_id>`.

## Persistence

Game objects are stored as YAML. Player files are written to `data/players` when clients disconnect and the server writes periodic autosave snapshots of the entire world to `data/world`. See [docs/persistence.md](docs/persistence.md) for format details.

## YAML Data Format

Rooms, items and NPCs are defined using YAML. A minimal room entry looks like:

```yaml
- id: start
  name: Central Hub
  description: The main arrival point of the station.
  components:
    room:
      exits:
        north: corridor_north
```

This structure maps directly into the component system discussed in
[docs/component_system.md](docs/component_system.md).

## Usage Guide

Once the server is running, connect to `http://localhost:5000` in your browser.
Type commands into the prompt to interact with the world. Useful commands include
`look`, `move <direction>`, `inventory` and `say <message>`.

## License

This project is released under the [MIT License](LICENSE).
