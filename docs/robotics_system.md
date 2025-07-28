# Robotics Department and Cyborg Mechanics

This module introduces a lightweight framework for the station's robotics lab. It tracks parts in storage and provides helpers for assembling cyborgs from a chassis and a set of modules. Robots consume power every tick so they must occasionally recharge at a dock.

## Key Concepts

- **RobotChassis** – defines module slots and power capacity.
- **RobotModule** – equipment installed on a cyborg that drains power.
- Modules can optionally be *remote controlled* and toggled on or off to
  conserve power. Inactive modules do not drain energy during a tick.
- **CyborgUnit** – a chassis with attached modules and a power cell.
- **RoboticsSystem** – manages part inventories, assembly and periodic upkeep.
- **DockingStation** – location that recharges cyborgs each tick.

Robots will automatically seek the nearest registered docking station when their
power falls below 20% of capacity. While docked they regain power each tick at
the station's recharge rate.

The system is intentionally small but acts as a starting point for more elaborate robotics gameplay in the future.

## Remote Control and Maintenance

Entire cyborg units may receive remote commands from the robotics console or AI. Commands like `shutdown` and `restart` affect every module at once. Engineers can also run `diagnostics` on a unit to get a simple status report and issue `repair` to fully recharge and reactivate all modules.

## Specialized Modules

New `SpecializedRobotModule` objects allow creating equipment with unique power usage and a description of what they do. For example a medical probe might drain 3 power per tick while enabling healing actions. Install these modules the same way as standard modules to expand your cyborg's capabilities.

## Medical Integration

Cyborgs equipped with a module whose functionality is `heal` can assist medical staff. The `heal_player` method on `RoboticsSystem` leverages these modules to heal a target player. Healing uses the genetics system, so mutations such as `regeneration` increase the amount restored.

## Maintenance Integration

Cyborg units are now tracked by the maintenance system using a built-in `MaintainableComponent`. Each tick applies wear based on active modules, and severe wear will render the cyborg inoperable until repaired. The `repair_unit` command fully services the cyborg and restores its condition to 100%.

## AI Integration

AI cores may register cyborg units and issue remote commands. A cyborg
checks the AI's laws before executing orders, refusing any directive
that conflicts with a higher-priority law (such as harming humans).

When linked to the robotics system, cyborgs can send diagnostic reports
back to the controlling AI which include module status and current
power level. These reports are published via the event bus so consoles
or scripts can react accordingly.
