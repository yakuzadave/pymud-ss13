import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from mudpy_interface import MudpyInterface
from engine import MudEngine
from systems.jobs import get_job_system
from systems.cargo import get_cargo_system, CargoSystem, SupplyVendor


def setup_env(tmp_path):
    old_world = world.WORLD
    world.WORLD = world.World(data_dir=str(tmp_path))
    old_cargo = get_cargo_system()
    # replace global cargo system
    import systems.cargo as cargo_mod
    cargo_mod.CARGO_SYSTEM = CargoSystem()
    cargo_mod.CARGO_SYSTEM.register_vendor(SupplyVendor("central", {"steel": 5}))
    return old_world, old_cargo


def teardown_env(old_world, old_cargo):
    import systems.cargo as cargo_mod
    cargo_mod.CARGO_SYSTEM = old_cargo
    world.WORLD = old_world


def test_commanding_officer_tracking():
    js = get_job_system()
    co = js.get_commanding_officer("command")
    assert co and co.job_id == "captain"


def setup_engine(tmp_path):
    interface = MudpyInterface(config_file=str(tmp_path/"cfg.yaml"), alias_dir=str(tmp_path/"aliases"))
    engine = MudEngine(interface)
    interface.connect_client("1")
    return interface, engine


def test_budget_permissions(tmp_path):
    old_w, old_c = setup_env(tmp_path)
    try:
        interface, engine = setup_engine(tmp_path)
        out = engine.process_command("1", "budget add engineering 10")
        assert "permission" in out.lower()
        js = get_job_system()
        js.assign_job("player_1", "captain")
        js.setup_player_for_job("player_1", "player_1")
        engine.process_command("1", "budget set engineering 100")
        engine.process_command("1", "budget add engineering 20")
        system = get_cargo_system()
        assert system.get_credits("engineering") == 120
    finally:
        teardown_env(old_w, old_c)


def test_finance_report(tmp_path):
    old_w, old_c = setup_env(tmp_path)
    try:
        interface, engine = setup_engine(tmp_path)
        js = get_job_system()
        js.assign_job("player_1", "captain")
        js.setup_player_for_job("player_1", "player_1")
        system = get_cargo_system()
        system.set_credits("engineering", 50)
        system.order_supply("engineering", "steel", 2, "central")
        report = engine.process_command("1", "finance")
        assert "engineering" in report
        assert "spent" in report
        assert system.get_spending("engineering") == 0
    finally:
        teardown_env(old_w, old_c)
