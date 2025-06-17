import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import GameObject
from components.ai import AIComponent, CyborgComponent


def setup_objs():
    w = world.get_world()
    ai_obj = GameObject(id="ai_test", name="AI", description="")
    ai_comp = AIComponent()
    ai_obj.add_component("ai", ai_comp)
    w.register(ai_obj)

    borg_obj = GameObject(id="borg_test", name="Borg", description="")
    borg_comp = CyborgComponent()
    borg_obj.add_component("cyborg", borg_comp)
    w.register(borg_obj)

    ai_comp.register_cyborg(borg_comp)
    return ai_comp, borg_comp


def teardown():
    w = world.get_world()
    for oid in ["ai_test", "borg_test"]:
        if oid in w.objects:
            del w.objects[oid]
            w.rooms.pop(oid, None)
            w.items.pop(oid, None)
            w.npcs.pop(oid, None)


def test_ai_law_order():
    ai = AIComponent()
    ai.add_law(2, "Obey orders")
    ai.add_law(1, "Never harm a human")
    assert ai.get_laws() == ["Never harm a human", "Obey orders"]


def test_cyborg_command():
    ai, borg = setup_objs()
    try:
        msg = ai.issue_command("borg_test", "patrol")
        assert "patrol" in msg
    finally:
        teardown()


def test_ai_check_action():
    ai = AIComponent()
    ai.add_law(1, "Never harm a human")
    assert not ai.check_action("harm human")
    assert ai.check_action("open door")


def test_cyborg_refuses_unlawful_command():
    ai, borg = setup_objs()
    ai.add_law(1, "Never harm a human")
    try:
        msg = ai.issue_command("borg_test", "harm human")
        assert "unable to comply" in msg.lower()
    finally:
        teardown()


def test_cyborg_status_report():
    ai, borg = setup_objs()
    try:
        status = borg.report_status()
        assert "power" in status
        assert status["power"] == 100
    finally:
        teardown()
