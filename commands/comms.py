from engine import register
from systems.communications import get_comms_system


@register("clearradiolog")
def clearradiolog_handler(interface, client_id, args):
    session = interface.client_sessions.get(client_id, {})
    if not session.get("is_admin", False):
        return "Permission denied."
    if not args:
        return "Usage: clearradiolog <channel>"
    system = get_comms_system()
    system.clear_radio_log(args.strip())
    return f"Radio log for {args.strip()} cleared."


@register("clearpdalog")
def clearpdalog_handler(interface, client_id, args):
    session = interface.client_sessions.get(client_id, {})
    if not session.get("is_admin", False):
        return "Permission denied."
    if not args:
        return "Usage: clearpdalog <device_id>"
    system = get_comms_system()
    system.clear_pda_log(args.strip())
    return f"PDA log for {args.strip()} cleared."


@register("pdakey")
def pdakey_handler(interface, client_id, args):
    session = interface.client_sessions.get(client_id, {})
    if not session.get("is_admin", False):
        return "Permission denied."
    if not args:
        return "Usage: pdakey <device_id>"
    system = get_comms_system()
    key = system.generate_pda_key(args.strip())
    if not key:
        return "Unknown PDA."
    return f"Key for {args.strip()}: {key}"
