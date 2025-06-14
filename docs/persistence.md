# Persistence and Autosave

Game objects are serialized to YAML when saved. Each file contains the object `id`, `name`, `description`, `location`, and a mapping of component data. Components provide a `to_dict` method and their values appear under the `components` key.

Player data is saved to `data/players/<id>.yaml` whenever a client disconnects. World snapshots are written periodically to `data/world/autosave_<timestamp>.yaml`.

The autosave interval defaults to one minute and runs in the background while the server is active.
