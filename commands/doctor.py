"""Doctor role specific commands."""

from engine import register
from events import publish
import world
from components.medical import MedicalScannerComponent


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


@register("scan")
def scan_handler(client_id: str, player: str = None, **kwargs):
    """Scan a patient with a medical scanner."""
    doctor = world.get_world().get_object(f"player_{client_id}")
    if not doctor:
        return "Player not found."
    doc_comp = doctor.get_component("player")
    if not doc_comp or doc_comp.role.lower() != "doctor":
        return "Only doctors can do that."
    if not player:
        return "Specify a patient to scan."

    target = world.get_world().get_object(f"player_{player}")
    if not target:
        return f"Patient '{player}' not found."
    tcomp = target.get_component("player")
    if not tcomp:
        return "Invalid patient."

    scanner_obj = None
    for item_id in doc_comp.inventory:
        obj = world.get_world().get_object(item_id)
        if obj and obj.get_component("medical_scanner"):
            scanner_obj = obj
            break
    if not scanner_obj:
        return "You need a medical scanner."

    scan_comp: MedicalScannerComponent = scanner_obj.get_component("medical_scanner")
    record = scan_comp.scan_player(tcomp)
    stats = record["stats"]
    lines = [
        f"Vitals for {target.name}:",
        f"Health: {stats.get('health', 0)}%",
        f"Oxygen: {stats.get('oxygen', 0)}%",
        f"Radiation: {stats.get('radiation', 0)}%",
    ]
    for part, dmg in record["damage"].items():
        for dtype, val in dmg.items():
            if val > 0:
                lines.append(f"{part} {dtype}: {val}")
    publish("scan_attempt", doctor_id=doctor.id, target=target.id)
    return "\n".join(lines)
