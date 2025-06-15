import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from engine import MudEngine
from mudpy_interface import MudpyInterface


def test_command_performance(benchmark, tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(
        config_file=str(cfg), alias_dir=str(tmp_path / "aliases")
    )
    engine = MudEngine(interface)
    interface.connect_client("1")

    def run():
        engine.process_command("1", "look")

    benchmark(run)
