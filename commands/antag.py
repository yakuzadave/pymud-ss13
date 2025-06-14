from engine import register


@register("antag")
def cmd_antag(interface, client_id, args):
    """Manage antagonist assignments."""
    session = interface.client_sessions.get(client_id, {})
    is_admin = session.get("is_admin", False)

    from systems.antagonists import get_antagonist_system

    system = get_antagonist_system()
    if not args or args.strip().lower() in {"list", "ls"}:
        antags = system.list_antagonists()
        if not antags:
            return "No antagonists are currently assigned."
        return "Antagonists: " + ", ".join(f"{a.player_id}:{a.role}" for a in antags)

    parts = args.split()
    cmd = parts[0].lower()

    if cmd == "assign":
        if not is_admin:
            return "You do not have permission to assign antagonists."
        if len(parts) < 2:
            return "Usage: antag assign <player_id>"
        pid = parts[1]
        system.assign_antagonist(pid)
        return f"{pid} has been assigned as a traitor."

    if cmd == "remove":
        if not is_admin:
            return "You do not have permission to remove antagonists."
        if len(parts) < 2:
            return "Usage: antag remove <player_id>"
        pid = parts[1]
        if system.remove_antagonist(pid):
            return f"Removed antagonist {pid}."
        return "Antagonist not found."

    if cmd == "complete":
        if len(parts) < 3:
            return "Usage: antag complete <player_id> <objective>"
        pid = parts[1]
        obj = " ".join(parts[2:])
        system.complete_objective(pid, obj)
        return f"Marked objective for {pid}."

    return f"Unknown antag command '{cmd}'."
