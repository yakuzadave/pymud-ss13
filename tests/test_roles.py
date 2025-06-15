from unittest import mock

import world
from world import GameObject
from components.player import PlayerComponent
from commands.engineer import repair_handler
from commands.doctor import heal_handler
from commands.security import restrain_handler
from systems.power import PowerGrid
from systems.atmosphere import AtmosphericSystem
import events


def setup_player(role):
    w = world.get_world()
    obj = GameObject(id="player_test", name="Tester", description="")
    comp = PlayerComponent(role=role)
    obj.add_component("player", comp)
    w.register(obj)
    return obj


def teardown_player():
    w = world.get_world()
    if "player_test" in w.objects:
        del w.objects["player_test"]
        w.players = {
            k: v for k, v in getattr(w, "players", {}).items() if k != "player_test"
        }


def test_power_grid_power_off_publishes(monkeypatch):
    grid = PowerGrid("g1", "Test")
    mock_pub = mock.Mock()
    monkeypatch.setattr(events, "publish", mock_pub)
    import systems.power as sp

    monkeypatch.setattr(sp, "publish", mock_pub)
    grid.power_off()
    mock_pub.assert_called_with("power_loss", grid_id="g1", affected_rooms=[])


def test_atmos_leak_publishes(monkeypatch):
    atmos = AtmosphericSystem()
    mock_pub = mock.Mock()
    monkeypatch.setattr(events, "publish", mock_pub)
    import systems.atmosphere as sa
    import systems.atmos as atmos_mod

    monkeypatch.setattr(sa, "publish", mock_pub)
    monkeypatch.setattr(atmos_mod, "publish", mock_pub)
    atmos.create_leak("room1", rate=1.0)
    mock_pub.assert_called_with("leak_started", room_id="room1", rate=1.0)


def test_engineer_command(monkeypatch):
    setup_player("engineer")
    try:
        result = repair_handler("test", target="panel")
        assert "repair" in result.lower()
    finally:
        teardown_player()


def test_doctor_command(monkeypatch):
    setup_player("doctor")
    try:
        result = heal_handler("test", target="crew")
        assert "heal" in result.lower()
    finally:
        teardown_player()


def test_security_command(monkeypatch):
    setup_player("security")
    try:
        result = restrain_handler("test", target="intruder")
        assert "restrain" in result.lower()
    finally:
        teardown_player()
