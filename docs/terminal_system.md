# Terminal System

The terminal system tracks computer terminals located around the station.
Each terminal exposes a simplified interface to an existing subsystem
such as engineering, cargo or security.

Terminals register themselves when the `TerminalComponent` is added to a
`GameObject`. Commands issued to a terminal are routed to the
appropriate console handler, allowing crew to access those features
remotely.

Example usage:

```python
from systems.terminal import get_terminal_system

result = get_terminal_system().execute("term1", "power")
print(result)  # Shows power grid status via the engineering console
```

The system publishes `terminal_registered` and `terminal_command` events
so other mechanics can audit usage or restrict access.
