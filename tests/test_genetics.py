import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.genetics import GeneticsSystem, get_genetics_system


def test_basic_mutation_cycle():
    system = GeneticsSystem()
    profile = system.get_profile("p1")
    profile.add_gene("strength", 5)
    system.mutate_player("p1", "hulk", severity=1.0)
    assert "hulk" in profile.mutations
    system.tick()
    assert profile.instability < 1.0
    # stabilize fully
    system.stabilize_player("p1", amount=1.0)
    system.tick()
    assert profile.instability == 0.0
    assert profile.mutations == []


def test_dna_scanning():
    system = GeneticsSystem()
    p1 = system.get_profile("p1")
    p1.add_gene("strength", 5)
    system.mutate_player("p1", "hulk")
    system.scan_dna("p2", "p1")
    assert system.apply_scanned_dna("p2")
    p2 = system.get_profile("p2")
    assert p2.genes.get("strength") == 5
    assert "hulk" in p2.mutations


def test_mutation_effect_applied(tmp_path):
    import world as world_mod
    from world import World, GameObject
    from components.player import PlayerComponent

    old_world = world_mod.WORLD
    world_mod.WORLD = World(data_dir=str(tmp_path))
    try:
        player = GameObject(id="p1", name="Tester", description="")
        player.add_component("player", PlayerComponent())
        world_mod.WORLD.register(player)

        system = get_genetics_system()
        system.profiles.clear()
        system.scanned_dna.clear()
        system.tick_interval = 0.0
        system.mutate_player("p1", "hulk")
        system.start()
        system.update()
        p_comp = player.get_component("player")
        assert p_comp.has_ability("smash")
        assert p_comp.stats["health"] > 100
    finally:
        world_mod.WORLD = old_world
