import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from integration import MudpyIntegration
from mudpy_interface import MudpyInterface
from components.door import DoorComponent
from world import GameObject
from components.player import PlayerComponent
from systems.jobs import get_job_system


def setup_world(tmp_path):
    old = world.WORLD
    world.WORLD = world.World(data_dir=str(tmp_path))
    return old


def teardown_world(old):
    world.WORLD = old


def test_default_job_assignment(tmp_path):
    old = setup_world(tmp_path)
    try:
        integ = MudpyIntegration(MudpyInterface())
        integ._on_client_connected("1")
        player = world.WORLD.get_object("player_1")
        comp = player.get_component("player")
        assert comp.role == "assistant"
        assert comp.access_level >= 10
    finally:
        teardown_world(old)


def test_door_respects_job_access(tmp_path):
    old = setup_world(tmp_path)
    try:
        job_system = get_job_system()
        player_obj = GameObject(id="player_test", name="Tester", description="")
        player_comp = PlayerComponent()
        player_obj.add_component("player", player_comp)
        world.WORLD.register(player_obj)
        job_system.assign_job(player_obj.id, "security")
        job_system.setup_player_for_job(player_obj.id, player_obj.id)
        door_obj = GameObject(id="door1", name="Door", description="")
        door = DoorComponent(is_open=False, is_locked=True, access_level=30)
        door_obj.add_component("door", door)
        msg = door.open(player_obj.id, access_code=player_comp.access_level)
        assert door.is_open
        assert "open" in msg.lower()
    finally:
        teardown_world(old)


def test_job_reassignment(tmp_path):
    old = setup_world(tmp_path)
    try:
        job_system = get_job_system()
        player_obj = GameObject(id="player_test2", name="Tester2", description="")
        comp = PlayerComponent()
        player_obj.add_component("player", comp)
        world.WORLD.register(player_obj)
        job_system.assign_job(player_obj.id, "assistant")
        job_system.setup_player_for_job(player_obj.id, player_obj.id)
        initial = comp.access_level
        job_system.assign_job(player_obj.id, "engineer")
        job_system.setup_player_for_job(player_obj.id, player_obj.id)
        assert comp.role == "engineer"
        assert comp.access_level > initial
    finally:
        teardown_world(old)


def test_antagonist_ability_present():
    job = get_job_system().jobs.get("traitor")
    assert job and "sabotage" in job.abilities


def test_new_jobs_registered():
    js = get_job_system()
    assert "geneticist" in js.jobs
    assert "virologist" in js.jobs
