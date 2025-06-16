from engine import register
from systems.jobs import JOB_SYSTEM


@register("manifest")
def cmd_manifest(interface, client_id, **_):
    """List connected players and their assigned jobs."""
    lines = []
    for job in JOB_SYSTEM.get_all_jobs():
        players = JOB_SYSTEM.get_players_by_job(job.job_id)
        if not players:
            continue
        names = []
        for pid in players:
            cid = pid.replace("player_", "")
            session = interface.client_sessions.get(cid, {})
            name = session.get("character") or f"Player_{cid}"
            names.append(name)
        names.sort()
        lines.append(f"{job.title}: {', '.join(names)}")
    if not lines:
        return "No crew members are online."
    lines.sort()
    return "Crew Manifest:\n" + "\n".join(lines)
