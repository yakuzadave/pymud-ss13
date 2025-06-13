# Subsystem Design

Subsystems model large station features such as power or atmosphere. Each subsystem is implemented as a Python module under `systems/`. They may maintain global state and register event handlers on startup.

The subsystem modules interact with game objects through their components. For example the `RandomEventSystem` selects events based on weights and publishes them via the event bus.
