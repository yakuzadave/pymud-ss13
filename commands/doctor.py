"""Doctor role specific commands."""

from engine import register
from events import publish
import world


@register("diagnose")
def diagnose_handler(client_id: str, player: str = None, **kwargs):
    """Provide a medical diagnosis for a target if you are a doctor."""
    doctor = world.get_world().get_object(f"player_{client_id}")
    if not doctor:
        return "Player not found."
    comp = doctor.get_component("player")
    if not comp or comp.role.lower() != "doctor":
        return "Only doctors can do that."
    if not player:
        return "Specify a patient to diagnose."

    target = world.get_world().get_object(f"player_{player}")
    if not target:
        return f"Patient '{player}' not found."
    tcomp = target.get_component("player")
    if not tcomp:
        return "Invalid patient."

    stats = tcomp.stats
    publish("diagnose_attempt", doctor_id=doctor.id, target=target.id)
    return (
        f"Vitals for {target.name}:\n"
        f"Health: {stats.get('health', 0)}%\n"
        f"Oxygen: {stats.get('oxygen', 0)}%\n"
        f"Radiation: {stats.get('radiation', 0)}%"
    )


@register("heal")
def heal_handler(client_id: str, target: str = None, **kwargs):
    """Heal a player if you are a doctor."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "doctor":
        return "Only doctors can do that."
    publish("heal_attempt", player_id=player.id, target=target)
    return f"You heal {target or 'the patient'}."
