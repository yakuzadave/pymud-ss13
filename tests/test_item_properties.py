from world import GameObject, World
from components.item import ItemComponent
import world


def test_examine_keycard_properties(tmp_path):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w
    item = GameObject(id="card1", name="Card", description="A test card")
    item.add_component(
        "item",
        ItemComponent(item_type="keycard", item_properties={"access_level": 42, "serial": "TEST-1"}),
    )
    w.register(item)
    text = item.get_component("item").examine("player")
    assert "Access level: 42" in text
    assert "Serial: TEST-1" in text


def test_examine_generic_properties(tmp_path):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w
    item = GameObject(id="uniform", name="Uniform", description="desc")
    item.add_component(
        "item",
        ItemComponent(item_type="apparel", item_properties={"armor_rating": 2, "slot": "body"}),
    )
    w.register(item)
    text = item.get_component("item").examine("player")
    assert "Armor rating: 2" in text
    assert "Slot: body" in text
