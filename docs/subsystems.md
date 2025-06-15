# Subsystem Design

Subsystems model large station features such as power or atmosphere. Each
subsystem lives in a Python module under `systems/` and usually exposes a
`start()`/`stop()` pair along with an `update()` method.  Many subsystems keep
their own global state and register event handlers when they start up.

The subsystem modules interact with game objects through their components.  For
example the `RandomEventSystem` selects events based on weights and publishes
them via the event bus.

When running `run_server.py` or `start_server.py` the core systems—power,
atmosphere and random events—are started automatically.  Background tasks tick
these subsystems so hazards and events occur without manual commands.

## Player and Admin Interactions

Most subsystems expose helpers that are invoked by commands.  Players operate
equipment or repair damage, while administrators can trigger events directly for
testing.  The systems below run automatically but also accept manual input:

- **PowerSystem** – rooms belong to power grids powered by generators, solars or
  batteries. Players may toggle breakers or repair generators. Admins can force
  outages or restore power. The system drains fuel and reports overloads
  automatically.
- **AtmosphericSystem** – tracks gas composition, vents and leaks. Players fix
  breaches or toggle ventilation. Admins can spawn fires or breaches. It
  continuously normalizes rooms and publishes hazard warnings.
- **RandomEventSystem** – loads definitions from `data/random_events.yaml` and
  fires them at intervals. Admins use `event list` and `event trigger` to manage
  events manually.
- **CommunicationsSystem** – manages radio channels, intercoms and PDAs.
  Players send messages via the `radio` or `pda` commands. Admins may jam
  channels or make high priority announcements.
- **CargoSystem** – vendors take supply orders that arrive after a delay. Cargo
  technicians place orders; the system processes deliveries and updates
  department inventories automatically.
- **RoboticsSystem** – handles cyborg assembly and recharging. Robotics staff
  build units from parts, while the system drains power each tick.
- **GeneticsSystem** – stores DNA profiles and active mutations. Scientists scan
  or apply genes with commands; instability decays over time without input.
- **AntagonistSystem** – tracks traitors and other hostile roles. Admins assign
  antagonists or check win conditions. The system keeps progress and fires a
  summary at round end.
- **SpaceExplorationSystem** – coordinates away missions via shuttle. Crew
  launch missions, then the system applies hazards and returns results.

Subsystem modules may be extended or replaced as the project grows. They
communicate using the event bus so features remain decoupled and easy to test.
