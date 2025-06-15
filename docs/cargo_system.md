# Cargo and Supply Chain System

This module implements a minimal logistics framework for ordering supplies and tracking station inventory.

## Features

- **Vendors** with simple pricing based on market demand
- **Supply orders** that arrive after a delay
- **Department inventories** stored per vendor/department
- **Market demand** controls pricing and can be adjusted dynamically

The system is intentionally lightweight but provides a foundation for more complex economic mechanics.

## Department Budgets

Each department has a credit balance tracked by the `CargoSystem`. Costs are
deducted when supplies are ordered and requests are blocked if a department does
not have enough credits.

Administrators can adjust these budgets using the `budget` command:

```text
budget list
budget set engineering 500
budget add science 100
```

## Ordering with Credits

Supplies are ordered through the API and will only succeed if the requesting
department can afford the cost:

```python
from systems.cargo import CargoSystem, SupplyVendor

system = CargoSystem()
system.register_vendor(SupplyVendor("central", {"steel": 5}))
system.set_credits("engineering", 20)

order = system.order_supply("engineering", "steel", 2, "central")
if not order:
    print("Insufficient credits")
```
