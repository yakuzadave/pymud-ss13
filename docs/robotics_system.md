# Robotics Department and Cyborg Mechanics

This module introduces a lightweight framework for the station's robotics lab. It tracks parts in storage and provides helpers for assembling cyborgs from a chassis and a set of modules. Robots consume power every tick so they must occasionally recharge at a dock.

## Key Concepts

- **RobotChassis** – defines module slots and power capacity.
- **RobotModule** – equipment installed on a cyborg that drains power.
- **CyborgUnit** – a chassis with attached modules and a power cell.
- **RoboticsSystem** – manages part inventories, assembly and periodic upkeep.

The system is intentionally small but acts as a starting point for more elaborate robotics gameplay in the future.
