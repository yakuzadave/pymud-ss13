# Genetics Department and DNA Mechanics

This module introduces a lightweight genetics system that tracks DNA profiles for players.  Each profile stores a set of genes and any active mutations.  DNA can be scanned from one player and applied to another to copy their traits.

`GeneticsSystem` exposes helpers for mutating or stabilizing a player.  Mutations increase genetic instability which slowly decays each tick.  When instability reaches zero the mutations clear automatically.  This provides a simple framework for experiments without deep integration yet.

The department can build upon this system by offering cloning or superpower mechanics in the future while remaining small enough for tests to cover the basics.
