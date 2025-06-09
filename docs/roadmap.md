# Project Roadmap

This roadmap outlines major phases and tasks required to build the core structure of PyMUD‑SS13. It expands on the development plan and acts as a checklist as the project evolves.

## 🔧 Phases & Tasks

### Phase 1 – Foundation Refactoring
- [ ] **Command Registry** – refactor `mudpy_interface.py` into `engine.py` and replace large `if/elif` chains with decorated handlers.
- [ ] **World Layer** – move YAML loading and object storage into `world.py` and centralize persistence in `persistence.py`.
- [ ] **Event Bus** – add `events.py` with `subscribe()` and `publish()` helpers and connect core loops to it.

### Phase 2 – Component System
- [ ] **GameObject Class** with a `components` dictionary and helper methods.
- [ ] **Core Components** – door control, access checks, containers, etc.
- [ ] **YAML → Components** – load component specs from `data/objects.yaml`.

### Phase 3 – Event‑Driven Systems
- [ ] **Atmospherics** system for pressure and gas handling.
- [ ] **Power Grid** with breakers and power events that auto‑lock doors.
- [ ] **Jobs & AI** providing crew roles and simple NPC behavior.
- [ ] **Random Event Manager** that periodically triggers station events.
- [ ] **Event Definitions** stored in `data/random_events.yaml` with weights and conditions.
- [ ] **Context‑Aware Triggers** reacting to power, atmosphere, or crew status.
- [ ] **Admin Controls** for manually firing or suppressing random events.

### Phase 4 – Dynamic In‑Game Scripting
- [ ] **Sandbox Engine** using RestrictedPython or Lua.
- [ ] **In‑World Verb API** for attaching new commands to objects.
- [ ] **Script Persistence** within save files.

### Phase 5 – Persistence Enhancements
- [ ] **State Serialization** of all object and component data.
- [ ] **Snapshotting** via periodic autosaves and shutdown hooks.

### Phase 6 – Web Client & UI
- [ ] **Command Interface** over WebSockets.
- [ ] **Grid‑Map Renderer** showing room layout.
- [ ] **Status Overlays** for door locks, atmos warnings, and power state.

### Phase 7 – Testing & Documentation
- [ ] **Unit Tests** for the engine, world, events, and scripts.
- [ ] **CI/CD Pipeline** with linting and automated tests.
- [ ] **Docs & Examples** describing the YAML formats and project setup.
