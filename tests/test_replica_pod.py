import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import World, GameObject
from components.player import PlayerComponent
from components.item import ItemComponent
from components.replica_pod import ReplicaPodComponent
from systems.genetics import get_genetics_system


def test_replica_pod_cloning(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        # original dead player
        player = GameObject(id="p1", name="Tester", description="")
        player.add_component("player", PlayerComponent())
        world.WORLD.register(player)
        genetics = get_genetics_system()
        profile = genetics.get_profile("p1")
        profile.add_gene("strength", 5)
        genetics.mutate_player("p1", "hulk")

        comp = player.get_component("player")
        comp.apply_damage("torso", "brute", 200)
        assert not comp.alive

        # create replica pod item manually
        pod = GameObject(id="pod1", name="Replica Pod", description="")
        pod.add_component("item", ItemComponent(is_takeable=True, is_usable=True))
        pod.add_component("replica_pod", ReplicaPodComponent())
        world.WORLD.register(pod)

        msg = pod.get_component("replica_pod").activate("p1")
        clone = world.WORLD.get_object("p1_podclone")
        assert clone is not None
        clone_profile = genetics.get_profile("p1_podclone")
        assert clone_profile.genes.get("strength") == 5
        assert "hulk" in clone_profile.mutations
        player_comp = clone.get_component("player")
        assert "podperson" == player_comp.role
        assert player_comp.stats.get("health") > 100
        assert player_comp.has_ability("smash")
    finally:
        world.WORLD = old_world
