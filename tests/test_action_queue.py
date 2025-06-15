import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from engine import MudEngine, action_queue
from mudpy_interface import MudpyInterface


def setup_engine(tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(
        config_file=str(cfg), alias_dir=str(tmp_path / "aliases")
    )
    engine = MudEngine(interface)
    interface.connect_client("1")
    return interface, engine


def test_action_queue_wait(tmp_path):
    interface, engine = setup_engine(tmp_path)
    action_queue.next_time.clear()
    out1 = engine.process_command("1", "move north")
    out2 = engine.process_command("1", "move north")
    assert "wait" in out2.lower()
    time.sleep(0.6)
    out3 = engine.process_command("1", "move north")
    assert "wait" not in out3.lower()
