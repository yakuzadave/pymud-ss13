import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from engine import MudEngine, action_queue
from mudpy_interface import MudpyInterface
from tests.ai_tools import AIPlayer


def setup_engine(tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(config_file=str(cfg), alias_dir=str(tmp_path / "aliases"))
    engine = MudEngine(interface)
    interface.connect_client("1")
    interface.connect_client("2")
    return interface, engine


def test_multiplayer_scenario(tmp_path):
    interface, engine = setup_engine(tmp_path)
    p1 = AIPlayer(engine, "1")
    p2 = AIPlayer(engine, "2")

    action_queue.next_time.clear()
    p1.run(["move north", "get keycard"])
    action_queue.next_time.clear()
    p2.run(["move north", "move east"])

    # Player2 should be blocked from entering research
    blocked = [out for cmd, out in p2.outputs if cmd == "move east"][0]
    assert "keycard" in blocked.lower()
    # Player1 can enter research
    out = engine.process_command("1", "move east")
    assert "research" in out.lower()
    assert interface.get_player_location("1") == "research"
    assert interface.get_player_location("2") == "corridor"

