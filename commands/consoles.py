from engine import register
from systems import (
    get_power_system,
    get_atmos_system,
    get_cargo_system,
    get_security_system,
)


@register("engconsole")
def engconsole_handler(client_id: str, action: str = "power", target: str = None, *, interface=None, **_):
    """Operate an engineering console to check or adjust station systems."""
    ps = get_power_system()
    atmos = get_atmos_system()

    action = (action or "power").lower()
    if action in {"power", "status"}:
        if not ps.grids:
            return "No power grids defined."
        lines = []
        for grid in ps.grids.values():
            state = "ON" if grid.is_powered else "OFF"
            lines.append(f"{grid.grid_id}: {grid.current_load:.0f}/{grid.capacity:.0f}% {state}")
        return "Power Grids:\n" + "\n".join(lines)
    if action == "usage":
        grid_id = target or next(iter(ps.grids)) if ps.grids else None
        if not grid_id:
            return "No power grids defined."
        graph = ps.get_usage_graph(grid_id)
        return f"Usage for {grid_id}:\n{graph}"
    if action in {"atmos", "atmosphere"}:
        room = target
        if not room and interface:
            room = interface.get_player_location(client_id)
        if not room:
            return "Specify a room for atmospheric readout."
        return atmos.describe_room_hazards(room)
    if action == "breaker":
        if not target:
            return "Usage: engconsole breaker <grid> <on|off>"
        parts = target.split()
        if len(parts) < 2:
            return "Usage: engconsole breaker <grid> <on|off>"
        grid_id, state = parts[0], parts[1].lower()
        active = state == "on"
        ps.on_grid_breaker_toggle(grid_id, active)
        status = "closed" if active else "opened"
        return f"Breaker for {grid_id} {status}."
    return "Unknown action."


@register("cargoconsole")
def cargoconsole_handler(client_id: str, action: str = "budgets", *args: str, **_):
    """Access cargo computer functions."""
    cargo = get_cargo_system()
    action = (action or "budgets").lower()
    if action == "budgets":
        if not cargo.department_credits:
            return "No budgets set."
        lines = [f"{d}: {c}" for d, c in cargo.department_credits.items()]
        return "Department Budgets:\n" + "\n".join(lines)
    if action == "order":
        if len(args) != 4:
            return "Usage: cargoconsole order <dept> <item> <qty> <vendor>"
        dept, item, qty_str, vendor = args
        try:
            qty = int(qty_str)
        except ValueError:
            return "Quantity must be a number."
        order = cargo.order_supply(dept, item, qty, vendor)
        if order:
            return f"Order placed for {item} x{qty} via {vendor}."
        return "Order failed."
    if action == "route":
        if not args:
            if not cargo.shuttle_routes:
                return "No routes defined."
            lines = [f"{rid}: {' -> '.join(stops)}" for rid, stops in cargo.shuttle_routes.items()]
            return "Shuttle Routes:\n" + "\n".join(lines)
        sub = args[0].lower()
        if sub == "set" and len(args) >= 3:
            route_id = args[1]
            stops = list(args[2:])
            cargo.set_route(route_id, stops)
            return f"Route {route_id} set."
        if sub == "clear" and len(args) == 2:
            cargo.clear_route(args[1])
            return f"Route {args[1]} cleared."
        return "Usage: cargoconsole route [set <id> <stops...>|clear <id>]"
    return "Unknown action."


@register("secconsole")
def secconsole_handler(client_id: str, action: str = "alerts", target: str = None, **_):
    """Interface with a security terminal."""
    sec = get_security_system()
    action = (action or "alerts").lower()
    if action == "alerts":
        alerts = sec.get_alerts()
        if not alerts:
            return "No active alerts."
        lines = [f"{a['type']} at {a['location']}" for a in alerts]
        return "Alerts:\n" + "\n".join(lines)
    if action == "crimes":
        if not sec.crimes:
            return "No crime records."
        lines = [f"{c.crime_id}: {c.severity} - {c.description}" for c in sec.crimes.values()]
        return "Crime Records:\n" + "\n".join(lines)
    if action == "pardon":
        if not target:
            return "Usage: secconsole pardon <player>"
        released = sec.release(target)
        return "Prisoner released." if released else "No such prisoner."
    return "Unknown action."
