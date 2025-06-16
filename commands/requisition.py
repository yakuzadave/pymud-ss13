from engine import register
import world
from systems.jobs import get_job_system
from systems.cargo import get_cargo_system


@register("requisition")
def requisition_handler(interface, client_id, args):
    """Request department credits for personal use."""
    try:
        amount = int(args.strip())
    except (ValueError, AttributeError):
        return "Usage: requisition <credits>"

    world_inst = world.get_world()
    player_obj = world_inst.get_object(f"player_{client_id}")
    if not player_obj:
        return "Player not found."

    job = get_job_system().get_player_job(player_obj.id)
    if not job:
        return "No job assigned."
    dept = job.department
    cargo = get_cargo_system()
    if cargo.get_credits(dept) < amount:
        return f"{dept} department lacks funds."

    cargo.add_credits(dept, -amount)
    stats = interface.get_player_stats(client_id)
    stats["credits"] = stats.get("credits", 0) + amount
    return f"Requisitioned {amount} credits from {dept}."

