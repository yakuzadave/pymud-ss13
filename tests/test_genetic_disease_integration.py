import world
from world import World, GameObject
from components.player import PlayerComponent
from systems.genetics import get_genetics_system
from systems.disease import DiseaseSystem


def test_immunity_prevents_infection(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        player = GameObject(id="p1", name="Pat", description="")
        comp = PlayerComponent()
        player.add_component("player", comp)
        world.WORLD.register(player)

        genetics = get_genetics_system()
        genetics.profiles.clear()
        genetics.scanned_dna.clear()
        genetics.mutate_player("p1", "immunity")

        disease = DiseaseSystem()
        disease.infect("p1", "flu")
        assert "flu" not in comp.diseases
    finally:
        world.WORLD = old_world
