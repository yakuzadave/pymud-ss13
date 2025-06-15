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


def test_disease_spread_and_cure_item(tmp_path, monkeypatch):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w

    p1 = GameObject(id="p1", name="p1", description="", location="room")
    c1 = PlayerComponent()
    p1.add_component("player", c1)
    w.register(p1)

    p2 = GameObject(id="p2", name="p2", description="", location="room")
    c2 = PlayerComponent()
    p2.add_component("player", c2)
    w.register(p2)

    disease_system = DiseaseSystem()
    monkeypatch.setattr("random.random", lambda: 0.0)
    disease_system.infect("p1", "flu")
    disease_system.tick()
    assert "flu" in c2.diseases

    medicine = GameObject(id="med", name="med", description="")
    medicine.add_component(
        "item",
        ItemComponent(
            is_takeable=True,
            is_usable=True,
            item_type="medical",
            item_properties={"cures": "flu"},
        ),
    )
    w.register(medicine)
    medicine.get_component("item").use("p2")
    assert "flu" not in c2.diseases


def test_protection_prevents_spread(tmp_path, monkeypatch):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w

    p1 = GameObject(id="p1", name="p1", description="", location="room")
    c1 = PlayerComponent()
    p1.add_component("player", c1)
    w.register(p1)

    p2 = GameObject(id="p2", name="p2", description="", location="room")
    c2 = PlayerComponent(inventory=["hazmat"])  # has protective gear
    p2.add_component("player", c2)
    w.register(p2)

    hazmat = GameObject(id="hazmat", name="hazmat", description="")
    hazmat.add_component(
        "item",
        ItemComponent(
            is_takeable=True,
            is_usable=True,
            item_type="apparel",
            item_properties={"biohazard_protection": True},
        ),
    )
    w.register(hazmat)

    disease_system = DiseaseSystem()
    monkeypatch.setattr("random.random", lambda: 0.0)
    disease_system.infect("p1", "flu")
    disease_system.tick()
    assert "flu" not in c2.diseases
