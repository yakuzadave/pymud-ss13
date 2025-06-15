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


def test_who_lists_players(tmp_path):
    interface, engine = setup_engine(tmp_path)
    interface.connect_client("2")

    interface.client_sessions["1"]["character"] = "Alice"
    interface.client_sessions["2"]["character"] = "Bob"

    out = engine.process_command("1", "who")
    assert "Alice" in out
    assert "Bob" in out
