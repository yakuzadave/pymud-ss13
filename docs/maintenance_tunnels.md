# Maintenance Tunnel Network

This station now includes a small network of dimly lit service tunnels.
These passages connect major departments without requiring the main
corridors.

```
maintenance_tunnel  - central junction between engineering and the new tunnels
maintenance_west    - links medbay and cargo bay
maintenance_north   - links security and the north airlock
```

The exits for several existing rooms were updated to hook into these
new tunnels. Medbay opens south into `maintenance_west`; Cargo Bay now
has a west hatch to the same tunnel. Security gains an additional west
exit into `maintenance_north`, while the north airlock allows access to
this tunnel from the exterior. From `maintenance_tunnel` you can travel
north to `maintenance_north` or west to `maintenance_west`.
