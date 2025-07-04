# Genetics Department and DNA Mechanics

This module introduces a lightweight genetics system that tracks DNA profiles for players.  Each profile stores a set of genes and any active mutations.  DNA can be scanned from one player and applied to another to copy their traits.

`GeneticsSystem` exposes helpers for mutating or stabilizing a player.  Mutations increase genetic instability which slowly decays each tick.  When instability reaches zero the mutations clear automatically.  The system now runs as a background task and applies mutation effects such as the **hulk** strength bonus.

Replica pods use this system when spawning a clone.  The clone inherits the target's DNA profile and any active mutations, immediately gaining their effects.  This provides a foundation for future superpower mechanics while remaining small enough for tests to cover the basics.

## Geneticist Role

Geneticists have access to the `mutate`, `stabilize`, `scan_dna` and `apply_dna` commands. These allow them to apply mutations to crew members, reduce genetic instability and copy DNA profiles. The job spawns in the science lab with a biometric scanner and standard science access.

## Random Events

The random event system can trigger incidents involving genetics or DNA labs, such as the **unstable_clone** event which causes harmful mutations.
