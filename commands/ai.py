"""Station AI command handlers."""

from engine import register
from systems.communications import get_comms_system
from systems.ai import (
    is_ai_client,
    get_camera_network,
    get_ai_law_system,
)


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


@register("ai_view")
def ai_view_handler(client_id: str, camera_id: str | None = None, **kwargs):
    """View camera feeds available on the network."""
    if not is_ai_client(client_id):
        return "Only the station AI can do that."
    network = kwargs.get("camera_network")
    if not network:
        network = get_camera_network()
    if camera_id:
        loc = network.get_feed(camera_id)
        if not loc:
            return "Camera not found."
        return f"{camera_id} viewing {loc}"
    feeds = network.list_feeds()
    if not feeds:
        return "No cameras online."
    lines = [f"{cid}: {loc}" for cid, loc in sorted(feeds.items())]
    return "\n".join(lines)


@register("set_law")
def set_law_handler(
    client_id: str, priority: int, *, directive: str = "", **kwargs
) -> str:
    """Add a new AI law."""
    if not directive:
        return "Specify a directive."
    if not is_ai_client(client_id):
        return "Only the station AI can do that."
    law_system = kwargs.get("ai_law_system")
    if not law_system:
        law_system = get_ai_law_system()
    law_system.add_law(priority, directive)
    return "Law added."
