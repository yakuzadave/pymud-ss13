# Object YAML Format

`data/objects.yaml` defines additional game objects that are not rooms or items. Each object entry may include any registered component. This allows doors, lockers and machinery to be described entirely in YAML.

Example:

```yaml
- id: maintenance_door
  name: Maintenance Door
  components:
    door:
      is_locked: true
      access_level: 30
- id: secure_locker
  name: Secure Locker
  components:
    container:
      capacity: 5
      is_locked: true
      access_level: 50
```

Load this file by calling `World.load_from_file("objects.yaml")`. The resulting objects can be interacted with using commands such as `open`, `lock`, `unlock` and the new `hack` command.
