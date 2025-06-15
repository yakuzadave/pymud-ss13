import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from world import World, GameObject, get_world
from components.room import RoomComponent
from components.door import DoorComponent
from components.npc import NPCComponent
from pathfinding import find_path


def build_world():
    w = get_world()
    # reset any existing objects
    w.objects.clear()
    w.rooms.clear()
    w.items.clear()
    w.npcs.clear()
    w.grid.tiles.clear()
    w.grid.positions.clear()

    room_a = GameObject(id="a", name="A", description="")
    room_a.add_component("room", RoomComponent(exits={"east": "b", "south": "d"}))
    door_comp = DoorComponent(is_open=False, is_locked=True, destination="b")
    room_a.add_component("door", door_comp)

    room_b = GameObject(id="b", name="B", description="")
    room_b.add_component("room", RoomComponent(exits={"east": "c"}))

    room_c = GameObject(id="c", name="C", description="")
    room_c.add_component("room", RoomComponent())

    room_d = GameObject(id="d", name="D", description="")
    room_d.add_component("room", RoomComponent(exits={"east": "c"}))

    for r in [room_a, room_b, room_c, room_d]:
        w.register(r)

    return w, door_comp


def test_find_path_around_locked_door():
    w, door = build_world()
    path = find_path(w, "a", "c")
    assert path == ["a", "d", "c"]

    # open the door and ensure direct path is used
    door.is_locked = False
    door.is_open = True
    path = find_path(w, "a", "c")
    assert path == ["a", "b", "c"]


def test_npc_movement_along_path():
    w, door = build_world()
    npc = GameObject(id="n", name="NPC", description="", location="a")
    npc_comp = NPCComponent()
    npc.add_component("npc", npc_comp)
    w.register(npc)

    npc_comp.set_goal("c")
    # step should compute path around locked door
    npc_comp.step()
    assert npc.location == "d"
    npc_comp.step()
    assert npc.location == "c"
