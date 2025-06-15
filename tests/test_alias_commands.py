import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from engine import MudEngine
from mudpy_interface import MudpyInterface


def setup_engine(tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(
        config_file=str(cfg), alias_dir=str(tmp_path / "aliases")
    )
    engine = MudEngine(interface)
    interface.connect_client("1")
    return interface, engine


def test_alias_resolves_and_unalias(tmp_path):
    interface, engine = setup_engine(tmp_path)
    out = engine.process_command("1", "alias h help")
    assert "Alias 'h'" in out

    direct = engine.process_command("1", "help")
    via_alias = engine.process_command("1", "h")
    assert via_alias == direct

    engine.process_command("1", "unalias h")
    assert "h" not in interface.aliases.get("1", {})
    unknown = engine.process_command("1", "h")
    assert "Unknown command" in unknown


def test_who_lists_connected_players(tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(
        config_file=str(cfg), alias_dir=str(tmp_path / "aliases")
    )
    engine = MudEngine(interface)
    interface.connect_client("1")
    interface.connect_client("2")

    out = engine.process_command("1", "who")
    name1 = interface.client_sessions["1"]["character"]
    name2 = interface.client_sessions["2"]["character"]
    assert name1 in out and name2 in out
