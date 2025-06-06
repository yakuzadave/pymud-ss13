# PyMUD-SS13 Development Plan

This document collects notes about the current codebase and outlines initial steps for building a modern text-based MUD inspired by **Space Station 13**. The repository already contains a basic engine with command parsing, YAML-based data files for rooms and items, and a simple web client using WebSockets.

## Observed Features

- **Command Parsing** via `parser.CommandParser` and YAML command specs (`data/commands.yaml`).
- **World Data** stored in YAML files (`data/rooms.yaml`, `data/items.yaml`).
- **Player and World Components** in the `components/` directory.
- **WebSocket Server** implemented with FastAPI (`mud_websocket_server.py`) and a browser client in `web_client/`.

## Immediate Goals

1. **Clean Up Documentation** – ensure README and other docs explain how to run and develop the project.
2. **Extend Game Mechanics** – continue fleshing out command handlers and world logic.
3. **Reference Existing MUD Engines** – examine open source MUD frameworks for ideas (see `resources.md`).
4. **Iterative Development** – start small with room navigation and inventory, then expand to complex systems inspired by Space Station 13.
5. **Command-Line Client** – provide a simple CLI for local testing of the engine.

