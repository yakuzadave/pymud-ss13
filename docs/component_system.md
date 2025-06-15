# Component System

Game objects are built from reusable components located in the `components/` directory. Each component encapsulates a small piece of behaviour and state. Objects such as rooms, items and players hold a dictionary of component instances.

Example:

```yaml
- id: bridge
  name: Command Bridge
  components:
    room:
      exits:
        north: corridor_north
```

Components keep their own data and provide helper functions used by commands and subsystems. This design lets new functionality be added by introducing a new component without rewriting existing classes.

Recent additions include a **CircuitComponent** for installing programmable circuits into items or machinery. These circuits rely on shells to hold logic components and tie into the power and USB subsystems.
