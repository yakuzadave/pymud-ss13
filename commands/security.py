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


@register("report")
def report_handler(
    client_id: str,
    *,
    description: str = "",
    suspect: str = None,
    severity: str = "minor",
    **kwargs,
):
    """Report a crime to the security system."""
    if not description:
        return "You must provide a description of the incident."
    sec = kwargs.get("security_system")
    if not sec:
        from systems.security import get_security_system

        sec = get_security_system()
    record = sec.report_crime(
        f"player_{client_id}", description, suspect_id=suspect, severity=severity
    )
    return f"Crime #{record.crime_id} reported."


@register("arrest")
def arrest_handler(client_id: str, target: str = None, duration: int = 60, **kwargs):
    """Arrest a target player for a duration in seconds."""
    if not target:
        return "Specify a target to arrest."
    sec = kwargs.get("security_system")
    if not sec:
        from systems.security import get_security_system

        sec = get_security_system()
    sec.arrest(target, duration)
    return f"{target} has been arrested for {duration} seconds."


@register("release")
def release_handler(client_id: str, target: str = None, **kwargs):
    """Release a prisoner if their sentence is over."""
    if not target:
        return "Specify a prisoner to release."
    sec = kwargs.get("security_system")
    if not sec:
        from systems.security import get_security_system

        sec = get_security_system()
    if sec.release(target):
        return f"{target} has been released."
    return "No such prisoner."


@register("evidence")
def evidence_handler(client_id: str, crime_id: int, *, note: str = "", **kwargs):
    """Add evidence to a crime record."""
    if not note:
        return "Describe the evidence."
    sec = kwargs.get("security_system")
    if not sec:
        from systems.security import get_security_system

        sec = get_security_system()
    if sec.add_evidence(crime_id, note):
        return "Evidence logged."
    return "Crime not found."


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
    lines = [
        f"{idx+1}. {a['type']} detected in {a['location']}"
        for idx, a in enumerate(alerts)
    ]
    return "Alerts:\n" + "\n".join(lines)


@register("access_log")
def access_log_handler(client_id: str, **kwargs):
    """Show recent access events."""
    system = get_security_system()
    log = system.get_access_log()
    lines = [f"{e['player']} -> {e['door']}" for e in log[-10:]]
    return "Access Log:\n" + "\n".join(lines) if lines else "No access events recorded."
