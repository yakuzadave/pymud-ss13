"""Player alias management commands."""

import logging
from engine import register

logger = logging.getLogger(__name__)


@register("alias")
def cmd_alias(interface, client_id, shortcut=None, command=None, **_):
    """Create or list personal command aliases."""
    if shortcut is None:
        aliases = interface.aliases.get(client_id, {})
        if not aliases:
            return "No aliases defined."
        lines = [f"{k} = {v}" for k, v in sorted(aliases.items())]
        return "Your aliases:\n" + "\n".join(lines)

    if command is None:
        return "Usage: alias <shortcut> <command>"

    shortcut = shortcut.strip()
    command = command.strip()
    if not shortcut or not command:
        return "Usage: alias <shortcut> <command>"

    interface.aliases.setdefault(client_id, {})[shortcut] = command
    if hasattr(interface, "save_aliases_for"):
        interface.save_aliases_for(client_id)
    return f"Alias '{shortcut}' set to '{command}'."


@register("unalias")
def cmd_unalias(interface, client_id, shortcut=None, **_):
    """Remove an existing alias."""
    if not shortcut:
        return "Usage: unalias <shortcut>"
    shortcut = shortcut.strip()
    aliases = interface.aliases.get(client_id, {})
    if shortcut in aliases:
        del aliases[shortcut]
        if hasattr(interface, "save_aliases_for"):
            interface.save_aliases_for(client_id)
        return f"Alias '{shortcut}' removed."
    return f"No alias named '{shortcut}'."
