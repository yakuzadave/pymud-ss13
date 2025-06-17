from engine import register
from systems.cargo import get_cargo_system
from systems.jobs import get_job_system


@register("budget")
def budget_handler(interface, client_id, args):
    """Adjust or list department budgets."""
    session = interface.client_sessions.get(client_id, {})
    job = get_job_system().get_player_job(f"player_{client_id}")
    rank = job.rank if job else 0

    system = get_cargo_system()
    if not args or args.strip().lower() in {"list", "ls"}:
        if not system.department_credits:
            return "No budgets set."
        lines = [f"{d}: {c}" for d, c in system.department_credits.items()]
        return "Department budgets:\n" + "\n".join(lines)

    if not session.get("is_admin", False) and rank < 80:
        return "You do not have permission to adjust budgets."

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


@register("finance")
def finance_handler(interface, client_id, args=None):
    """Report department credits and recent spending."""
    session = interface.client_sessions.get(client_id, {})
    job = get_job_system().get_player_job(f"player_{client_id}")
    rank = job.rank if job else 0
    if not session.get("is_admin", False) and rank < 50:
        return "Insufficient rank for finance report."
    system = get_cargo_system()
    if not system.department_credits:
        return "No financial data."
    lines = []
    for dept, credits in sorted(system.department_credits.items()):
        spent = system.get_spending(dept)
        lines.append(f"{dept}: {credits} credits, spent {spent}")
    system.clear_spending()
    return "Financial Summary:\n" + "\n".join(lines)


@register("trade")
def trade_handler(interface, client_id, args=None):
    """Transfer goods between departments for credits."""
    if not args:
        return "Usage: trade <from> <to> <item> <qty> <price>"

    parts = args.split()
    if len(parts) != 5:
        return "Usage: trade <from> <to> <item> <qty> <price>"

    from_dept, to_dept, item, qty_str, price_str = parts
    try:
        qty = int(qty_str)
        price = int(price_str)
    except ValueError:
        return "Quantity and price must be numbers."

    cargo = get_cargo_system()
    success = cargo.transfer_supply(from_dept, to_dept, item, qty, price)
    if success:
        return f"Transferred {item} x{qty} from {from_dept} to {to_dept}."
    return "Transfer failed."

