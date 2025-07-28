import world
from world import World, GameObject
from components.player import PlayerComponent
from systems.genetics import get_genetics_system


def test_regeneration_boosts_healing(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    player = GameObject(id="p1", name="Tester", description="")
    comp = PlayerComponent()
    player.add_component("player", comp)
    world.WORLD.register(player)

    try:
        genetics = get_genetics_system()
        genetics.profiles.clear()
        genetics.scanned_dna.clear()
        genetics.mutate_player("p1", "regeneration")

        comp.apply_damage("torso", "brute", 10)
        comp.heal_damage("torso", "brute", 5)

        assert comp.body_parts["torso"]["brute"] == 2.5
    finally:
        world.WORLD = old_world
