import systems.gas_sim as gs
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import systems.gas_sim as gs
from components.player import PlayerComponent
from world import GameObject


def test_pressure_equalization():
    grid = gs.AtmosGrid(2, 1)
    high = grid.get_tile(0, 0)
    low = grid.get_tile(1, 0)
    high.gas.pressure = 120.0
    low.gas.pressure = 80.0
    grid.step(rate=0.5)
    assert high.gas.pressure < 120.0
    assert low.gas.pressure > 80.0


def test_player_breathe_affects_room():
    grid = gs.AtmosGrid(1, 1)
    room_tile = grid.get_tile(0, 0)
    player_obj = GameObject(id="p1", name="p", description="")
    comp = PlayerComponent()
    player_obj.add_component("player", comp)
    comp.breathe(room_tile)
    assert room_tile.gas.composition["oxygen"] < 21.0
    assert room_tile.gas.composition["co2"] > 0.04

