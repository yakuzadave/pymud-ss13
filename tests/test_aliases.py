import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from engine import MudEngine
from mudpy_interface import MudpyInterface


def setup_engine(tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(config_file=str(cfg), alias_dir=str(tmp_path / "aliases"))
    engine = MudEngine(interface)
    interface.connect_client("1")
    return interface, engine


def test_alias_create_use_remove(tmp_path):
    interface, engine = setup_engine(tmp_path)
    out = engine.process_command("1", "alias h help")
    assert "Alias 'h'" in out
    assert interface.aliases["1"]["h"] == "help"

    orig = engine.process_command("1", "help")
    via_alias = engine.process_command("1", "h")
    assert via_alias == orig

    engine.process_command("1", "unalias h")
    assert "h" not in interface.aliases.get("1", {})
    unknown = engine.process_command("1", "h")
    assert "Unknown command" in unknown


def test_alias_persistence(tmp_path):
    interface, engine = setup_engine(tmp_path)
    engine.process_command("1", "alias x help")
    interface.disconnect_client("1")

    # new session loads alias
    interface2 = MudpyInterface(config_file=str(tmp_path / "config.yaml"), alias_dir=str(tmp_path / "aliases"))
    interface2.connect_client("1")
    engine2 = MudEngine(interface2)
    assert interface2.aliases["1"]["x"] == "help"
    out = engine2.process_command("1", "x")
    assert "Unknown command" not in out
