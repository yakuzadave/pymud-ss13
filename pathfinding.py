from __future__ import annotations

"""Simple pathfinding helpers."""

from collections import deque
from typing import List, Optional

from world import World


def find_path(world: World, start: str, goal: str) -> List[str]:
    """Return a list of room IDs from start to goal using BFS.

    If no path exists, an empty list is returned. Doors that are locked or
    closed block movement.
    """
    if start == goal:
        return [start]

    queue: deque[List[str]] = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        current = path[-1]
        if current == goal:
            return path
        room = world.get_object(current)
        if not room:
            continue
        room_comp = room.get_component("room")
        if not room_comp:
            continue
        for _dir, dest in room_comp.exits.items():
            # check for a door blocking this exit
            door = room.get_component("door")
            if (
                door
                and door.destination == dest
                and (door.is_locked or not door.is_open)
            ):
                continue
            if dest not in visited:
                visited.add(dest)
                queue.append(path + [dest])
    return []
