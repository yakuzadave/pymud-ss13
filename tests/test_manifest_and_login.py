import asyncio
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import world
from mud_server import MudServer
from mudpy_interface import MudpyInterface
import account_system as accounts
from systems.jobs import get_job_system
from commands.admin import cmd_manifest
from world import World


class DummyWebSocket:
    def __init__(self, messages):
        self.messages = list(messages)
        self.sent = []

    async def send(self, msg):
        self.sent.append(msg)

    async def recv(self):
        return self.messages.pop(0)

    def __hash__(self):
        return id(self)


def setup_world(tmp_path):
    old = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    return old


def teardown_world(old):
    world.WORLD = old


def test_login_assigns_selected_job(tmp_path, monkeypatch):
    old = setup_world(tmp_path)
    acc_file = tmp_path / "accounts.yaml"
    monkeypatch.setattr(accounts, "ACCOUNTS_FILE", acc_file)
    try:
        js = get_job_system()
        js.reset_assignments()
        server = MudServer()
        ws = DummyWebSocket(["tester", "secret", "engineer"])
        asyncio.run(server._login(ws))
        player_id = f"player_{id(ws)}"
        job = js.get_player_job(player_id)
        assert job and job.job_id == "engineer"
        asyncio.run(server._logout(ws, id(ws)))
    finally:
        teardown_world(old)


def test_manifest_lists_players(tmp_path):
    interface = MudpyInterface(config_file=str(tmp_path / "c.yaml"), alias_dir=str(tmp_path / "a"))
    interface.connect_client("1")
    interface.connect_client("2")
    interface.client_sessions["1"]["character"] = "Alice"
    interface.client_sessions["2"]["character"] = "Bob"

    js = get_job_system()
    js.reset_assignments()
    js.assign_job("player_1", "engineer")
    js.setup_player_for_job("player_1", "player_1")
    js.assign_job("player_2", "doctor")
    js.setup_player_for_job("player_2", "player_2")

    out = cmd_manifest(interface, "1")
    assert "Engineer" in out
    assert "Doctor" in out
    assert "Alice" in out and "Bob" in out
