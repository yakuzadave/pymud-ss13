# Space Exploration and Away Missions

This module introduces lightweight support for off-station exploration.
Shuttles can travel to procedurally defined sites, where random hazards may
occur each tick. Away teams should wear EVA suits to monitor their oxygen
supply. Radiation pockets, meteor showers and alien spores are common threats
and sites may contain random deposits of ore, crystal or ice. New resources can
spawn over time so diligent crews can harvest them for the station. The system
acts as a hook for future expansion and integration with more robust gameplay.

## Key Components

- **Shuttle** – manages navigation, fuel consumption and docking events.
- **AwaySite** – represents a destination with environmental hazards and
  resource deposits.
- **EVASuit** – tracks oxygen levels and suffers damage from severe hazards.
- **AwayMission** – combines a shuttle, a site and a list of crew members.

`SpaceExplorationSystem` ties these pieces together so game logic can launch a
mission and advance it with regular ticks. Resources gathered during missions
are returned to the station when the shuttle docks.


