from world import GameObject, get_world
from components.player import PlayerComponent
from components.item import ItemComponent


def test_vacuum_protection_from_space_suit():
    w = get_world()
    w.objects.clear()
    player = GameObject(id="p", name="p", description="")
    comp = PlayerComponent()
    player.add_component("player", comp)
    w.register(player)

    suit = GameObject(id="s", name="suit", description="")
    suit.add_component("item", ItemComponent(item_properties={"vacuum_protection": True}))
    w.register(suit)

    comp.equipment["body"] = "s"
    assert comp.has_vacuum_protection()
