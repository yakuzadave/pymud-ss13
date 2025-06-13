# Event Bus

The engine exposes a simple event bus used by systems to publish and respond to in-game events. Random station events are loaded from `data/random_events.yaml` and dispatched through this bus.

Handlers subscribe to events and perform actions when the event is fired. Administrators can trigger events manually using the `event` command, or they occur automatically according to their configured weights.
