# Project Roadmap

This roadmap outlines major phases and tasks required to build the core structure of PyMUD‑SS13. It expands on the development plan and acts as a checklist as the project evolves.

## 🔧 Phases & Tasks

### Phase 1 – Foundation Refactoring
- [x] **Command Registry** – refactored into `engine.py` with decorated handlers.
- [x] **World Layer** – YAML loading and object storage live in `world.py`; persistence is centralised in `persistence.py`.
- [x] **Event Bus** – `events.py` provides `subscribe()` and `publish()` and core loops are connected.

### Phase 2 – Component System
- [x] **GameObject Class** with a `components` dictionary and helper methods.
- [x] **Core Components** – door control, access checks, containers and more.
- [x] **YAML → Components** – object specs load component data from YAML files.

### Phase 3 – Event‑Driven Systems
- [x] **Atmospherics** system for pressure and gas handling.
- [x] **Power Grid** with breakers and power events that auto‑lock doors.
- [x] **Jobs & AI** providing crew roles and basic NPC behavior.
- [x] **Random Event Manager** periodically triggers station events.
- [x] **Communications Network** with radios, intercoms and PDAs.
- [x] **Event Definitions** stored in `data/random_events.yaml` with weights and conditions.
- [x] **Context‑Aware Triggers** reacting to power, atmosphere, or crew status.
- [x] **Admin Controls** for manually firing or suppressing random events.

### Phase 4 – Dynamic In‑Game Scripting
- [x] **Sandbox Engine** using RestrictedPython.
- [x] **In‑World Verb API** for attaching new commands to objects.
- [x] **Script Persistence** within save files.

### Phase 5 – Persistence Enhancements
- [x] **State Serialization** of all object and component data.
- [x] **Snapshotting** via periodic autosaves and shutdown hooks.

### Phase 6 – Web Client & UI
- [x] **Command Interface** over WebSockets.
- [x] **Grid‑Map Renderer** showing room layout.
- [x] **Status Overlays** for door locks, atmos warnings, and power state.

### Phase 7 – Testing & Documentation
- [x] **Unit Tests** for the engine, world, events, and scripts.
- [x] **CI/CD Pipeline** with linting and automated tests.
- [x] **Docs & Examples** describing the YAML formats and project setup.

### Phase 8 – Advanced Systems
- [ ] **Robotics & Cyborg Expansion** – extend robotics modules with remote control and power management.
- [ ] **Genetics & Cloning** – integrate the genetics system with cloning mechanics and mutation effects.
- [x] **Economy & Cargo** – deepen the trading system with market events and player-driven supply chains.
- [ ] **Space Exploration** – broaden away missions with random hazards and resource gathering.
- [ ] **Enhanced Frontend** – improve the browser UI with inventory management and richer map interactions.
- [ ] **Account Management** – persistent user accounts with authentication and admin permissions.
