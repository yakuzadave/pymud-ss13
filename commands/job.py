"""Job management commands."""

import world
from engine import register
from systems.jobs import get_job_system


@register("job")
def cmd_job(interface, client_id, args):
    """Assign or list jobs."""
    system = get_job_system()
    if not args or args.strip().lower() in {"list", "ls"}:
        names = ", ".join(sorted(j.job_id for j in system.get_all_jobs()))
        return f"Available jobs: {names}"

    parts = args.split()
    if parts[0] in {"set", "assign"}:
        if len(parts) == 2:
            target_id = f"player_{client_id}"
            job_id = parts[1]
        elif len(parts) == 3:
            target_id = (
                f"player_{parts[1]}" if not parts[1].startswith("player_") else parts[1]
            )
            job_id = parts[2]
        else:
            return "Usage: job set <job_id> or job set <player> <job_id>"

        world_inst = world.get_world()
        player_obj = world_inst.get_object(target_id)
        if not player_obj:
            return "Player not found."
        job = system.assign_job(target_id, job_id)
        if not job:
            return f"Unknown job '{job_id}'."

        player_comp = player_obj.get_component("player")
        if player_comp:
            player_comp.role = job.job_id
        setup_msg = system.setup_player_for_job(target_id, player_obj.id)
        return setup_msg or f"{player_obj.name} is now {job.title}."

    return "Usage: job [list] | job set <job_id>"
