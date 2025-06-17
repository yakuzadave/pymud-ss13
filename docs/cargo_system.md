# Cargo and Supply Chain System

This module implements a minimal logistics framework for ordering supplies and tracking station inventory.

## Features

- **Vendors** with simple pricing based on market demand
- **Supply orders** that arrive after a delay
- **Department inventories** stored per vendor/department
- **Market demand** controls pricing and can be adjusted dynamically
- **Fluctuating economy** with periodic demand changes and temporary supply shortages
- **Market events** triggered via the event bus
- **Player transfers** move goods between departments for credits
- **Trade command** lets crew exchange items via `trade <from> <to> <item> <qty> <price>`

The system is intentionally lightweight but provides a foundation for more complex economic mechanics.

## Department Budgets

Each department has a credit balance tracked by the `CargoSystem`. Costs are
deducted when supplies are ordered and requests are blocked if a department does
not have enough credits.

Crew members may requisition personal spending credits from their department
using the `requisition` command. The command checks the player's job role to
determine which department budget to draw from.

Administrators can adjust these budgets using the `budget` command:

```text
budget list
budget set engineering 500
budget add science 100
```

Only characters with a high **rank** (or administrators) may modify budgets.
Each `Job` has a `rank` attribute and the `JobSystem` keeps track of the
commanding officer for each department. Rank also gates the new `finance`
command which reports departmental spending and then resets the counters.

```text
finance
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

Crew can request spending money with:

```text
requisition 20
```

## Market Fluctuations

Call `update_economy()` periodically to simulate shifting demand and random
supply shortages. When a shortage is active, vendors run out of stock and orders
for the affected item are blocked until the shortage ends.

## Market Events

Economy-related random events may fire via the global event bus. These events
adjust demand values or trigger new shortages by calling `market_event`. The
`CargoSystem` listens for these events automatically.

Example event payload:

```python
from events import publish

publish("market_event", item="steel", demand_delta=1.5, shortage=3)
```

Two predefined economic events exist in `data/random_events.yaml`:

- `demand_spike` increases demand for electronics.
- `trade_embargo` creates a temporary steel shortage.

## Player Supply Transfers

Players can move items between departments to create their own supply chains.
Use `transfer_supply(from_dept, to_dept, item, qty, price)` or the `trade`
command to exchange goods and credits.

```
trade mining engineering ore 5 2
```

The above example trades 5 units of ore from mining to engineering for 2 credits
each.
