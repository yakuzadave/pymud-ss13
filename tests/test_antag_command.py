import os
import sys
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from engine import MudEngine
from mudpy_interface import MudpyInterface
from commands.antag import cmd_antag


def setup(tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(config_file=str(cfg), alias_dir=str(tmp_path / "a"))
    engine = MudEngine(interface)
    interface.connect_client("1")
    return interface, engine


def test_antag_command_assign_and_list(tmp_path, monkeypatch):
    interface, engine = setup(tmp_path)
    interface.client_sessions["1"]["is_admin"] = True

    mock_pub = mock.Mock()
    monkeypatch.setattr("events.publish", mock_pub)
    import systems.antagonists as sa
    monkeypatch.setattr(sa, "publish", mock_pub)

    out = cmd_antag(interface, "1", "assign 1")
    assert "traitor" in out

    out = cmd_antag(interface, "1", "list")
    assert "1:traitor" in out
