import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from world import World, GameObject
from components.container import ContainerComponent
import events


def test_spatial_queries_and_movement(monkeypatch):
    w = World(data_dir="data")
    a = GameObject(id="a", name="A", description="", position=(0, 0))
    b = GameObject(id="b", name="B", description="", position=(1, 0))
    w.register(a)
    w.register(b)
    assert "b" in w.objects_near("a", 1.1)
    w.move_object_xy("b", 5, 5)
    assert "b" not in w.objects_near("a", 1.1)
    assert w.line_of_sight("a", "b") is True


def test_object_events(monkeypatch):
    log = []
    monkeypatch.setattr(events, "publish", lambda *args, **kw: log.append((args, kw)))
    import world as world_mod

    monkeypatch.setattr(
        world_mod, "publish", lambda *args, **kw: log.append((args, kw))
    )
    w = World(data_dir="data")
    obj = GameObject(id="o", name="Obj", description="", position=(0, 0))
    w.register(obj)
    obj.move_to("room1")
    w.move_object_xy("o", 1, 1)
    w.remove("o")
    names = [a[0][0] for a in log]
    assert "object_created" in names
    assert "object_moved" in names
    assert "object_moved_xy" in names
    assert "object_destroyed" in names


def test_nested_containers():
    locker = GameObject(id="locker", name="Locker", description="")
    outer = ContainerComponent(capacity=2)
    locker.add_component("container", outer)

    box = GameObject(id="box", name="Box", description="")
    inner = ContainerComponent(capacity=2)
    box.add_component("container", inner)

    assert outer.add_item("box")
    assert inner.add_item("wrench")
    assert outer.items == ["box"]
    assert inner.items == ["wrench"]
