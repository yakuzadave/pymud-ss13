"""Utilities for AI related functionality."""

from systems.jobs import get_job_system


def is_ai_client(client_id: str) -> bool:
    """Return True if the given client is assigned the AI job."""
    player_id = client_id
    if not player_id.startswith("player_"):
        player_id = f"player_{client_id}"
    job = get_job_system().get_player_job(player_id)
    return bool(job and job.job_id == "ai")
