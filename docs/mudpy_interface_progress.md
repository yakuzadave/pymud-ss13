# Mudpy Interface Progress

This document tracks recent updates to `mudpy_interface.py` and outlines potential follow‑up tasks.

## Recent Changes
- **Inventory Preservation** – `connect_client` no longer overwrites an existing inventory. New players receive a default starter kit only if no inventory is recorded.
- **Inventory Accessor** – Added `get_player_inventory(client_id)` to return the list of item IDs a player currently carries.
- **Map Command Validation** – Verified that calling `map` works without raising errors after these changes.

## Next Steps
- **Persistence Integration** – Ensure inventories persist across server restarts by expanding the autosave routine.
- **Expanded Equipment Handling** – Provide helper functions for equipping and removing gear rather than directly mutating dictionaries.
- **Tests** – Add unit tests covering `get_player_inventory` and inventory initialization logic to guard against regressions.
- **Documentation** – Update command references and player guides to mention the map functionality and inventory requirements.

