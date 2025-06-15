"""Replica Pod component for cloning dead players into podpeople."""

from typing import Optional

from world import get_world, GameObject
from components.player import PlayerComponent
from systems.genetics import get_genetics_system, GeneticProfile


class ReplicaPodComponent:
    """When activated by a dead player, spawns a podperson clone."""

    def __init__(self) -> None:
        self.owner: Optional[GameObject] = None

    def activate(self, player_id: str) -> str:
        world = get_world()
        player = world.get_object(player_id)
        if not player:
            return "Nobody to clone."
        player_comp = player.get_component("player")
        if not player_comp:
            return "Invalid target."
        if player_comp.alive:
            return "The pod is dormant to the living."

        genetics = get_genetics_system()
        original_profile = genetics.get_profile(player_id)

        clone_id = f"{player_id}_podclone"
        if world.get_object(clone_id):
            return "A clone already exists."

        clone = GameObject(
            id=clone_id,
            name=f"Podperson {player.name}",
            description="A freshly grown plant-based clone.",
            location=player.location,
        )
        clone.add_component("player", PlayerComponent(role="podperson"))
        world.register(clone)

        genetics.profiles[clone_id] = GeneticProfile(
            genes=dict(original_profile.genes),
            mutations=list(original_profile.mutations),
            instability=original_profile.instability,
        )

        return "A podperson clone emerges from the pod."
