"""Commands for manipulating circuits."""

from engine import register
from systems.circuits import get_circuit_system


@register("circuit")
def circuit_handler(client_id: str, *args, **_):
    """Manage circuits.

    Usage:
        circuit insert <circuit_id> <component>
        circuit toggle <circuit_id> on|off
    """
    system = get_circuit_system()
    if not args:
        return "Usage: circuit <insert|toggle> ..."
    cmd = args[0].lower()
    if cmd == "insert":
        if len(args) < 3:
            return "Usage: circuit insert <circuit_id> <component>"
        cid = args[1]
        comp = args[2]
        if system.insert_component(cid, comp):
            return f"Inserted {comp} into {cid}."
        return "Unable to insert component."
    if cmd == "toggle":
        if len(args) < 3:
            return "Usage: circuit toggle <circuit_id> on|off"
        cid = args[1]
        state = args[2].lower() in {"on", "true", "1"}
        if system.toggle(cid, state):
            return f"Circuit {cid} {'activated' if state else 'deactivated'}."
        return "Circuit not found."
    return f"Unknown circuit command '{cmd}'."
