# MUDpy with WebSocket Interface

This project extends the MUDpy game engine with a WebSocket interface. Players can connect via a modern web browser instead of a Telnet client.

## Features

- **Textual TUI Client**: Modern terminal user interface with multiple switchable views (F1-F4), keyboard shortcuts, and real-time updates. See [TUI Documentation](tui_client/README.md) for details.
- **MUDpy Integration**: Interfaces with the MUDpy game engine.
- **Persistent Storage**: Uses YAML for configuration and data files.
- **Web-Based Frontend**: Connect through a browser using WebSockets.
- **NPC Data**: Non-player characters defined in `data/npcs.yaml`.
- **User-defined Aliases**: Create shortcuts with `alias` and remove them with `unalias`. Aliases persist between sessions.
- **See Who's Online**: View active players at any time with the `who` command.
- **Command History and Dark Mode** support.
- **Responsive Design** for desktop and mobile.
- **Admin Event Control**: List and trigger random events using the `event` command.
- **Grid Map & Status Overlays**: View a simple station layout with door lock,
  atmosphere, and power indicators via WebSocket updates.
- **Automatic Subsystems**: Power, atmosphere and random events tick in the background when the server runs.
- **Cargo System**: Order supplies through vendors and track department inventory.
- **Away Missions**: Basic shuttle travel and off-station exploration with environmental hazards.
- **Physics System**: Materials react to pressure and temperature with damage cascading to nearby structures.
- **Robotics System**: Build cyborg units from parts and manage their modules.
- **Botany Lab**: Grow plants and harvest produce with a lightweight botany
  system.
- **Kitchen & Cafe**: Cook meals for the crew using YAML recipes and serve them in the cafe.
- **Food Guide**: Example cooking mechanics and recipes are covered in
  `docs/food_guide.md`.
- **Drink Guide**: Bartending recipes are listed in `docs/drink_guide.md`.
- **Hydroponics Guide**: Items and plant crafting are described in `docs/hydroponics_guide.md`.
- **Plumbing System**: Automated fluid transfer is explained in `docs/plumbing_setup.md`.
- **Circuits Guide**: Basic electronic logic with shells and components is covered in `docs/circuits_guide.md`.
- **Bartender Role & Bar**: Mix drinks and keep the bar running smoothly.
- **Botanist Commands**: Plant seeds, fertilize and analyze crops with new botany mechanics.
- **Medical Treatment**: Diagnose and heal crewmates using doctor commands.
- **Security Enforcement**: Restrain suspects and manage arrests through security actions.
- **Engineering Repairs**: Fix equipment and prototype new devices with engineering tasks.

## Requirements

- Python 3.11+
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

### Terminal UI Client

For a terminal-based interface, launch the Textual TUI client:

```bash
python tui_client.py
```

The TUI provides multiple views accessible via function keys:
- **F1**: Game view - Main gameplay interface
- **F2**: Inventory view - Item management
- **F3**: Map view - Visual station map
- **F4**: Help view - Command reference
- **F5**: Chat view - Multi-channel communication
- **F10**: Quit

See [tui_client/README.md](tui_client/README.md) for complete documentation.

## Accounts

User credentials are stored in `data/accounts.yaml`. When a new
username logs in the server will create an entry in this file with a
hashed password. Administrators are determined by the
`administrator` flag on their account. The first account named
`admin` is automatically granted administrator status. You can edit
`accounts.yaml` manually while the server is offline to promote or
demote users.

## Player Arrival

When you first connect the server greets you aboard a small shuttle bound for
Space Station Alpha. After providing your account credentials the shuttle crew
asks which job you would like to perform. Type the job name from the list to
select your role. Once chosen the job system equips your character and moves you
to the appropriate department. Other players will see a message that a new crew
member has arrived.

### Grid Map and Overlays

Click the **Map** button in the web client to request the current station layout
from the server. Rooms are shown in a simple grid with icons indicating locked
doors, atmospheric hazards, and power loss. These overlays update in real time
based on WebSocket events.

To load a different station layout, set the `STATION_LAYOUT` environment
variable to an alternate rooms YAML file before starting the server:

```bash
STATION_LAYOUT=rooms_beta.yaml python run_server.py
```

The default file `rooms.yaml` holds the Alpha layout while `rooms_beta.yaml`
provides a smaller example map. The Alpha map now includes a small network
of maintenance tunnels linking engineering, medbay, cargo and security.

### Inventory Panel

Press the **Inventory** button in the web client to open a sidebar listing your
carried items and equipped gear. Selecting an item reveals its description along
with **Use** and **Drop** buttons so you can manage your inventory directly from
the browser.


## Running Tests

Install project dependencies and run the suite with pytest:

```bash
pip install -r requirements.txt
pytest
```

Automated gameplay scenarios are located in `tests/test_ai_gameplay.py` and
use simple AI players to run through common interactions. Performance
benchmarks can be executed with:

```bash
pytest tests/test_performance.py --benchmark-only
```


## Random Events

Random station events are defined in `data/random_events.yaml`.  Each entry in
that file specifies an event name, its weight, and optional conditions for it to
occur.  The server loads these definitions at startup and the event manager
periodically picks one based on their weights, automatically running the
corresponding logic. The interval between checks is configured on the
`RandomEventSystem` and defaults to 60 seconds.

Once the server is running, events are scheduled automatically so random
incidents will occur periodically without needing any admin commands.

Administrators can view available events with `event list` and manually trigger
them using `event trigger <event_id>`.

## Antagonists

The `AntagonistSystem` tracks traitors or other hostile roles. Admins can assign
traitors using the `antag assign <player_id>` command and review all active
antagonists with `antag list`. Objectives can be marked complete with
`antag complete <player_id> <objective>`, allowing simple win/loss checks at
round end.

## Round Management

The `RoundManager` controls the flow of each game round. When the server
starts you can specify a game mode with `--mode`. The default mode is
`traitor`, but a simple `cult` mode is also available.

```bash
python run_server.py --mode cult
```

The manager tracks antagonists via the `AntagonistSystem` and checks win
conditions when `end_round()` is called.

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

Additional game objects such as doors or containers can be listed in
`data/objects.yaml`. Each entry specifies components to attach. For example:

```yaml
- id: secure_locker
  name: Secure Locker
  components:
    container:
      capacity: 5
      is_locked: true
      access_level: 50
```

Loading this file with `World.load_from_file("objects.yaml")` makes the locker
interactable with commands like `open` or `hack`.

## Usage Guide

Once the server is running, connect to `http://localhost:5000` in your browser.
Type commands into the prompt to interact with the world. Useful commands include
`look`, `move <direction>`, `inventory` and `say <message>`.
You can create shortcuts for long commands with `alias <shortcut> <command>` and remove them with
`unalias <shortcut>`. Aliases are saved per player and persist between sessions.
The `who` command lists all players currently online.

## Modding

Mods live in the `mods/` directory. Each mod must contain a `mod.yaml` file describing the mod and may include `content` and `scripts` folders. Mods are automatically loaded when the world is initialized. You can also load them manually using `ModManager`:

```python
from mod_manager import ModManager
manager = ModManager()
manager.discover()
manager.load_all()
```

The included `example_mod` demonstrates adding a new item.

## License

This project is released under the [MIT License](LICENSE).
