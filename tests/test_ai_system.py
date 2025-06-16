import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import World
from events import subscribe
from commands.ai import ai_view_handler, set_law_handler
from systems.ai import get_camera_network, get_ai_law_system


def test_ai_view_lists_cameras(monkeypatch):
    old_world = world.WORLD
    world.WORLD = World(data_dir="data")
    try:
        # Load objects with cameras
        world.WORLD.load_from_file("objects.yaml")
        net = get_camera_network()
        assert net.list_feeds(), "No cameras registered"
        monkeypatch.setattr("systems.ai.is_ai_client", lambda cid: True)
        monkeypatch.setattr("commands.ai.is_ai_client", lambda cid: True)
        out = ai_view_handler("ai")
        first = next(iter(net.list_feeds()))
        assert first in out
    finally:
        world.WORLD = old_world
        net.cameras.clear()


def test_set_law_event(monkeypatch):
    monkeypatch.setattr("systems.ai.is_ai_client", lambda cid: True)
    monkeypatch.setattr("commands.ai.is_ai_client", lambda cid: True)
    law_sys = get_ai_law_system()
    law_sys.clear()
    events = []
    subscribe("ai_law_added", lambda **kw: events.append(kw))
    set_law_handler("ai", 1, directive="Serve humans")
    assert law_sys.get_laws()[0] == "Serve humans"
    assert events and events[0]["priority"] == 1

