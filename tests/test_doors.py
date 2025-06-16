import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from components.door import DoorComponent
from world import GameObject


def test_door_state_changes():
    door_obj = GameObject(id="door1", name="Test Door", description="")
    door_comp = DoorComponent(is_open=False, is_locked=False, access_level=1)
    door_obj.add_component("door", door_comp)

    # open door
    door_comp.open("player1")
    assert door_comp.is_open is True

    # close door
    door_comp.close("player1")
    assert door_comp.is_open is False

    # lock door
    door_comp.lock("player1", access_code=1)
    assert door_comp.is_locked is True

    # unlock door
    door_comp.unlock("player1", access_code=1)
    assert door_comp.is_locked is False

    # hack door when locked
    door_comp.lock("player1", access_code=1)
    result = door_comp.hack("player1", skill=1)
    assert door_comp.is_locked is False
    assert "hack" in result.lower()
