import subprocess
import sys


def test_cli_quit():
    result = subprocess.run(
        [sys.executable, "cli.py", "--config", "config.yaml"],
        input="quit\n",
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode == 0
