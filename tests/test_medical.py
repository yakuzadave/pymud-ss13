import world
from world import GameObject, World
from components.player import PlayerComponent
from components.item import ItemComponent
from systems.disease import DiseaseSystem


def test_healing_and_disease(tmp_path):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w
    player_obj = GameObject(id="p1", name="p1", description="p1")
    comp = PlayerComponent()
    player_obj.add_component("player", comp)
    w.register(player_obj)

    bandage_item = GameObject(id="bandage1", name="bandage", description="band")
    bandage_item.add_component(
        "item",
        ItemComponent(
            is_takeable=True,
            is_usable=True,
            item_type="medical",
            item_properties={"heal_type": "brute", "heal_amount": 5},
        ),
    )
    w.register(bandage_item)
    comp.apply_damage("torso", "brute", 10)
    bandage_item.get_component("item").use("p1")
    assert comp.body_parts["torso"]["brute"] < 10

    disease_system = DiseaseSystem()
    disease_system.infect("p1", "flu")
    disease_system.tick()
    assert "flu" in comp.diseases
