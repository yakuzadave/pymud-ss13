"""Command to operate a station terminal."""

from engine import register
from systems import get_terminal_system


@register("terminal")
def terminal_handler(client_id: str, terminal_id: str, *args: str, **_):
    """Execute a command on a station terminal."""
    if not terminal_id:
        return "Usage: terminal <id> <command> [args...]"
    if not args:
        return "Specify a command to run."
    command = args[0]
    out = get_terminal_system().execute(terminal_id, command, *args[1:])
    return out or "No response."
