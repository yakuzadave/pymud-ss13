import os
import sys
import yaml

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from components.container import ContainerComponent
from world import GameObject
from persistence import save_game_object


def test_container_updates_and_persistence(tmp_path):
    obj = GameObject(id="box1", name="Box", description="")
    container = ContainerComponent(capacity=5)
    obj.add_component("container", container)

    assert container.add_item("wrench") is True
    assert container.add_item("screwdriver") is True
    assert container.items == ["wrench", "screwdriver"]

    assert container.remove_item("wrench") is True
    assert container.items == ["screwdriver"]

    save_path = tmp_path / "box.yaml"
    save_game_object(obj, save_path)
    with open(save_path) as f:
        data = yaml.safe_load(f)

    saved_items = data["components"]["container"]["items"]
    assert saved_items == container.items
