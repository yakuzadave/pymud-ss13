from unittest import mock

import world
from world import GameObject
from components.player import PlayerComponent
from commands.engineer import repair_handler, diagnostics_handler, reroute_handler, seal_handler
from commands.doctor import heal_handler, diagnose_handler
from commands.security import restrain_handler
from commands.geneticist import mutate_handler, stabilize_handler
from commands.virologist import infect_handler, cure_handler
from systems.power import PowerGrid
from systems.atmosphere import AtmosphericSystem
import systems
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


def test_diagnose_command(monkeypatch):
    setup_player("doctor")
    target = GameObject(id="player_target", name="Target", description="")
    target.add_component("player", PlayerComponent())
    world.get_world().register(target)
    try:
        result = diagnose_handler("test", player="target")
        assert "health" in result.lower()
    finally:
        world.get_world().remove("player_target")
        teardown_player()


def test_security_command(monkeypatch):
    setup_player("security")
    try:
        result = restrain_handler("test", target="intruder")
        assert "restrain" in result.lower()
    finally:
        teardown_player()


def test_engineer_diagnostics(monkeypatch):
    setup_player("engineer")
    class DummyInterface:
        def get_player_location(self, cid):
            return "room1"

    try:
        result = diagnostics_handler("test", interface=DummyInterface())
        assert "power" in result.lower()
    finally:
        teardown_player()


def test_reroute_command(monkeypatch):
    setup_player("engineer")
    ps = systems.get_power_system()
    ps.grids.clear()
    g1 = PowerGrid("g1", "A")
    g1.add_room("room1")
    g2 = PowerGrid("g2", "B")
    ps.register_grid(g1)
    ps.register_grid(g2)
    try:
        result = reroute_handler("test", room="room1", grid="g2")
        assert "rerouted" in result.lower()
        assert "room1" in ps.grids["g2"].rooms
    finally:
        ps.grids.clear()
        teardown_player()


def test_seal_command(monkeypatch):
    setup_player("engineer")
    atmos = systems.get_atmos_system()
    atmos.leaks = []
    atmos.create_leak("room1", rate=1.0)
    try:
        result = seal_handler("test", room="room1")
        assert "seal" in result.lower()
        assert not atmos.leaks
    finally:
        atmos.leaks = []
        teardown_player()


def test_geneticist_commands(tmp_path):
    world.WORLD = world.World(data_dir=str(tmp_path))
    setup_player("geneticist")
    target = GameObject(id="player_target", name="Target", description="")
    target.add_component("player", PlayerComponent())
    world.WORLD.register(target)
    try:
        mutate_handler("test", mutation="hulk", player="target")
        profile = systems.get_genetics_system().get_profile("player_target")
        assert "hulk" in profile.mutations
        stabilize_handler("test", player="target", amount=1.0)
        assert profile.instability == 0
    finally:
        world.WORLD.remove("player_target")
        teardown_player()


def test_virologist_commands(tmp_path):
    world.WORLD = world.World(data_dir=str(tmp_path))
    setup_player("virologist")
    target = GameObject(id="player_tgt", name="Tgt", description="")
    target.add_component("player", PlayerComponent())
    world.WORLD.register(target)
    try:
        infect_handler("test", player="tgt", disease="flu")
        comp = target.get_component("player")
        assert "flu" in comp.diseases
        cure_handler("test", player="tgt", disease="flu")
        assert "flu" not in comp.diseases
    finally:
        world.WORLD.remove("player_tgt")
        teardown_player()
