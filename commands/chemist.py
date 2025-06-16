"""Chemist role specific commands."""

from engine import register
import world
from systems.chemistry import get_chemistry_system


@register("mix")
def mix_handler(client_id: str, *chemicals, **kwargs):
    """Mix chemicals if player is a chemist."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "chemist":
        return "Only chemists can do that."
    if not chemicals:
        return "Specify chemicals to mix."
    system = get_chemistry_system()
    return system.craft(client_id, list(chemicals))

@register("transfer")
def transfer_handler(client_id: str, source: str = None, dest: str = None, **kwargs):
    """Transfer all reagents from one container to another."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "chemist":
        return "Only chemists can do that."
    if not source or not dest:
        return "Specify source and destination containers."
    w = world.get_world()
    src = w.get_object(source)
    dst = w.get_object(dest)
    if not src or not dst:
        return "Container not found."
    sc = src.get_component("chemical_container")
    dc = dst.get_component("chemical_container")
    if not sc or not dc:
        return "Both must be chemical containers."
    sc.transfer_to(dc)
    return f"Transferred reagents from {source} to {dest}."


@register("dispense")
def dispense_handler(
    client_id: str,
    reagent: str = None,
    target: str = None,
    dispenser: str = "chemical_dispenser",
    amount: float = 1.0,
    **kwargs,
):
    """Dispense a reagent into a container from a dispenser."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "chemist":
        return "Only chemists can do that."
    if not reagent or not target:
        return "Specify a reagent and target container."
    w = world.get_world()
    disp_obj = w.get_object(dispenser)
    targ_obj = w.get_object(target)
    if not disp_obj or not targ_obj:
        return "Object not found."
    dcomp = disp_obj.get_component("chemical_container")
    tcomp = targ_obj.get_component("chemical_container")
    if not dcomp or not tcomp:
        return "Invalid container."
    if not dcomp.remove_reagent(reagent, amount):
        return "Reagent not available."
    tcomp.add_reagent(reagent, amount)
    return f"Dispensed {reagent} into {target}."


from systems.advanced_chemistry import ReactionChain
from systems.chemical_reactions import ChemicalContainerComponent


@register("react")
def react_handler(
    client_id: str,
    chain: ReactionChain = None,
    chamber: str = "reaction_chamber",
    temperature: float = None,
    **kwargs,
):
    """Run a reaction chain inside a reaction chamber."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "chemist":
        return "Only chemists can do that."
    w = world.get_world()
    chamber_obj = w.get_object(chamber)
    if not chamber_obj:
        return "Chamber not found."
    ccomp = chamber_obj.get_component("chemical_container")
    if not isinstance(ccomp, ChemicalContainerComponent):
        return "Invalid chamber."
    if temperature is not None:
        ccomp.heat(temperature)
    if chain:
        available = dict(ccomp.contents)
        produced = chain.process(available, ccomp)
        ccomp.contents = available
        if produced:
            return f"Produced {' '.join(produced)}."
        return "No reaction occurred."
    return "Chamber ready."
