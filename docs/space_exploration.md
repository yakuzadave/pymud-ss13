# Space Exploration and Away Missions

This module introduces very small-scale support for off-station exploration.
Shuttles can travel to procedurally defined sites, where random hazards may
occur each tick. Away teams should wear EVA suits to monitor their oxygen
supply. The system is intentionally lightweight and acts as a hook for future
expansion.

## Key Components

- **Shuttle** – manages navigation, fuel consumption and docking events.
- **AwaySite** – represents a destination with environmental hazards and
  resource deposits.
- **EVASuit** – tracks oxygen levels during extravehicular activity.
- **AwayMission** – combines a shuttle, a site and a list of crew members.

`SpaceExplorationSystem` ties these pieces together so game logic can launch a
mission and advance it with regular ticks.


