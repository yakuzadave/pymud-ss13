from engine import register
import world
from systems.genetics import get_genetics_system


def _check_role(client_id: str):
    obj = world.get_world().get_object(f"player_{client_id}")
    if not obj:
        return None, None
    comp = obj.get_component("player")
    if not comp or comp.role.lower() != "geneticist":
        return None, None
    return obj, comp


@register("mutate")
def mutate_handler(client_id: str, mutation: str = None, player: str = None, severity: float = 1.0, **_):
    obj, comp = _check_role(client_id)
    if not obj:
        return "Only geneticists can do that."
    if not mutation:
        return "Specify a mutation."
    target_id = f"player_{player}" if player else obj.id
    w = world.get_world()
    target = w.get_object(target_id)
    if not target:
        return "Target not found."
    system = get_genetics_system()
    system.mutate_player(target_id, mutation, float(severity))
    return f"Applied {mutation} to {target.name}."


@register("stabilize")
def stabilize_handler(client_id: str, player: str = None, amount: float = 0.5, **_):
    obj, comp = _check_role(client_id)
    if not obj:
        return "Only geneticists can do that."
    target_id = f"player_{player}" if player else obj.id
    w = world.get_world()
    if not w.get_object(target_id):
        return "Target not found."
    system = get_genetics_system()
    system.stabilize_player(target_id, float(amount))
    return f"Stabilized {player or 'self'}." 


@register("scan_dna")
def scan_dna_handler(client_id: str, target: str = None, **_):
    obj, _ = _check_role(client_id)
    if not obj:
        return "Only geneticists can do that."
    if not target:
        return "Specify a target to scan."
    tid = f"player_{target}"
    system = get_genetics_system()
    if not system.scan_dna(obj.id, tid):
        return "Scan failed."
    return f"DNA of {target} recorded."


@register("apply_dna")
def apply_dna_handler(client_id: str, **_):
    obj, _ = _check_role(client_id)
    if not obj:
        return "Only geneticists can do that."
    system = get_genetics_system()
    if system.apply_scanned_dna(obj.id):
        return "DNA applied."
    return "No DNA data." 
