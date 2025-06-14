"""Security role commands."""

from engine import register
from events import publish
import world
from systems.security import get_security_system

@register("restrain")
def restrain_handler(client_id: str, target: str = None, **kwargs):
    """Restrain a target if player is security."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "security":
        return "Only security officers can do that."
    publish("restrain_attempt", player_id=player.id, target=target)
    return f"You restrain {target or 'the suspect'}."


@register("view_cameras")
def view_cameras_handler(client_id: str, **kwargs):
    """List registered security cameras."""
    system = get_security_system()
    cams = [f"{cid}: {cam.location}" for cid, cam in system.cameras.items()]
    return "Cameras:\n" + "\n".join(cams) if cams else "No cameras online."


@register("view_alerts")
def view_alerts_handler(client_id: str, **kwargs):
    """Show pending security alerts."""
    system = get_security_system()
    alerts = system.get_alerts()
    if not alerts:
        return "No active alerts."
    lines = [f"{idx+1}. {a['type']} detected in {a['location']}" for idx, a in enumerate(alerts)]
    return "Alerts:\n" + "\n".join(lines)


@register("access_log")
def access_log_handler(client_id: str, **kwargs):
    """Show recent access events."""
    system = get_security_system()
    log = system.get_access_log()
    lines = [f"{e['player']} -> {e['door']}" for e in log[-10:]]
    return "Access Log:\n" + "\n".join(lines) if lines else "No access events recorded."
