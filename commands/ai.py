"""Station AI command handlers."""

from engine import register
from systems.communications import get_comms_system
from systems.ai import is_ai_client


@register("announce_ai")
def announce_ai_handler(client_id: str, *, message: str = "", **kwargs):
    """Broadcast an AI station announcement."""
    if not message:
        return "Specify a message to announce."
    if not is_ai_client(client_id):
        return "Only the station AI can do that."
    comms = kwargs.get("comms_system")
    if not comms:
        comms = get_comms_system()
    comms.announce(message, priority=10)
    return "Announcement sent."
