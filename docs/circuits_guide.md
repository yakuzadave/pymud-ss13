# Circuit Mechanics and Components

This guide outlines a lightweight circuit system inspired by Space Station 13. Circuits consist of an **integrated circuit** powered by a **power cell** and installed in a variety of shells. Each shell determines how many logic components can be inserted and whether special features are available.

## Basic Parts

| Item | Description | Function |
|------|-------------|---------|
| Integrated Circuit | Foundation for all circuits | Core processing unit for circuit logic |
| Power Cell | Energy source | Insert with left-click, remove with screwdriver |
| Shell | Housing for circuit | Provides interfaces and component capacity |
| Multitool | Circuit interface tool | Access circuit programming interface |
| Components | Logic elements | Perform specific functions within circuits |

## Shell Examples

| Shell | Size | Components | Special Features |
|-------|------|-----------|------------------|
| Compact Remote | Small | 25 | Hand-held with button outputs |
| Wall-Mounted Case | Medium | 50 | Can draw APC power |
| Bot Shell | Large | 100 | Mobile platform for complex circuits |
| BCI Shell | Very Large | 500 | Brain‑computer implant |

Other shells such as scanners, cameras and remote controls provide similar limits but different interfaces.

## Signal Types

Circuits use a variety of signals:

- **Signal** – electrical pulse to trigger actions.
- **Number** – numeric value used for maths or timers.
- **String** – ASCII text for messages or commands.
- **Entity** – reference to a specific object or player.
- **List/Associative List** – collections of values for batch processing.

## Logic Components

Common components include comparison checks, boolean logic, arithmetic, clocks and delays. Data manipulation modules offer list processing, string formatting and variable storage. Sensors allow circuits to react to the world, such as GPS location, health status or spoken messages.

## USB Devices

Circuits can connect to station devices via USB cables. Lightswitches, status displays, quantum pads and numerous consoles expose inputs and outputs for more advanced automation.

## Usage Tips

- Store repeated values in variables and reference them with getters.
- Use lists to handle multiple targets or items at once.
- Delay and clock components create timed reactions.
- Voice activators paired with comparisons make simple voice‑controlled doors.

The circuit framework integrates with existing components by letting shells act like powered items or stationary machinery. The **CircuitSystem** now manages power drain and USB connections so circuits can interact with devices in the world.

## In-game Commands

Use the following commands to work with assembled circuits:

- `circuit insert <circuit_id> <component>` – add a logic component to a circuit.
- `circuit toggle <circuit_id> on|off` – activate or deactivate a circuit.
- `circuit connect <circuit_id> <device_id>` – link a circuit to powered equipment via USB.
