import asyncio
import asyncio
import sys
import os
import yaml

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import GameObject, World
from mudpy_interface import MudpyInterface
import integration
from persistence import autosave_loop


def test_disconnect_saves_player(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        integ = integration.MudpyIntegration(MudpyInterface())
        integ._on_client_connected("99")
        integ._on_client_disconnected("99")
        save_file = tmp_path / "players" / "player_99.yaml"
        assert save_file.exists()
        with open(save_file) as f:
            data = yaml.safe_load(f)
        assert data["id"] == "player_99"
    finally:
        world.WORLD = old_world


def test_autosave_contains_all_objects(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        world.WORLD.register(GameObject(id="a", name="a", description=""))
        world.WORLD.register(GameObject(id="b", name="b", description=""))
        asyncio.run(autosave_loop(world.WORLD, interval=0, iterations=1, prefix="snap"))
        snaps = list((tmp_path / "world").glob("snap_*.yaml"))
        assert snaps, "autosave file not created"
        with open(snaps[0]) as f:
            data = yaml.safe_load(f)
        assert len(data) == len(world.WORLD.objects)
    finally:
        world.WORLD = old_world


def test_init_world_loads_saved_players(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        from components.player import PlayerComponent
        from persistence import save_game_object

        player = GameObject(id="player_42", name="Loaded", description="")
        player.add_component("player", PlayerComponent())
        save_game_object(player, tmp_path / "players" / "player_42.yaml")

        world.WORLD = World(data_dir=str(tmp_path))
        integ = integration.MudpyIntegration(MudpyInterface())
        assert integ.world.get_object("player_42") is not None
    finally:
        world.WORLD = old_world

