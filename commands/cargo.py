from engine import register
from systems.cargo import get_cargo_system


@register("budget")
def budget_handler(interface, client_id, args):
    """Adjust or list department budgets (admin only)."""
    session = interface.client_sessions.get(client_id, {})
    if not session.get("is_admin", False):
        return "You do not have permission to adjust budgets."

    system = get_cargo_system()
    if not args or args.strip().lower() in {"list", "ls"}:
        if not system.department_credits:
            return "No budgets set."
        lines = [f"{d}: {c}" for d, c in system.department_credits.items()]
        return "Department budgets:\n" + "\n".join(lines)

    parts = args.split()
    if len(parts) != 3 or parts[0] not in {"set", "add"}:
        return "Usage: budget [list] | budget set <department> <amount> | budget add <department> <amount>"

    cmd, dept, amt_str = parts
    try:
        amount = int(amt_str)
    except ValueError:
        return "Amount must be a number."

    if cmd == "set":
        system.set_credits(dept, amount)
        return f"{dept} budget set to {system.get_credits(dept)}"
    else:
        system.add_credits(dept, amount)
        return f"{dept} budget is now {system.get_credits(dept)}"
