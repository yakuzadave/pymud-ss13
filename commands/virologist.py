from engine import register
import world
from systems.disease import get_disease_system


def _check_role(client_id: str):
    obj = world.get_world().get_object(f"player_{client_id}")
    if not obj:
        return None, None
    comp = obj.get_component("player")
    if not comp or comp.role.lower() != "virologist":
        return None, None
    return obj, comp


@register("infect")
def infect_handler(client_id: str, player: str = None, disease: str = None, **_):
    obj, comp = _check_role(client_id)
    if not obj:
        return "Only virologists can do that."
    if not player or not disease:
        return "Specify a target and disease."
    tid = f"player_{player}"
    w = world.get_world()
    if not w.get_object(tid):
        return "Target not found."
    system = get_disease_system()
    system.infect(tid, disease)
    return f"{player} infected with {disease}."


@register("cure")
def cure_handler(client_id: str, player: str = None, disease: str = None, **_):
    obj, comp = _check_role(client_id)
    if not obj:
        return "Only virologists can do that."
    if not player or not disease:
        return "Specify a target and disease."
    tid = f"player_{player}"
    w = world.get_world()
    if not w.get_object(tid):
        return "Target not found."
    system = get_disease_system()
    system.cure(tid, disease)
    return f"{player} cured of {disease}."


@register("diagnose_disease")
def diagnose_disease_handler(client_id: str, player: str = None, **_):
    obj, comp = _check_role(client_id)
    if not obj:
        return "Only virologists can do that."
    if not player:
        return "Specify a patient."
    tid = f"player_{player}"
    w = world.get_world()
    target = w.get_object(tid)
    if not target:
        return "Target not found."
    tcomp = target.get_component("player")
    if not tcomp:
        return "Invalid target."
    if not tcomp.diseases:
        return f"{player} is healthy."
    return ", ".join(tcomp.diseases)
