# Web Client Map and Overlays

The web interface can display a simple grid of rooms. Press the **Map** button to
request the layout from the server. Each cell shows the first letter of the room
name. Icons indicate important status information:

- **Lock icon** – a door in that room is locked.
- **Alert icon** – atmospheric hazards are present.
- **Zap‑off icon** – the power grid for that room is down.

The grid updates automatically whenever the server broadcasts door, atmospherics
or power events. Refresh the page if the map becomes out of sync.

Hovering over a cell now highlights it for easier navigation. Clicking a room
outlines the cell and prints its details to the terminal. Use the **Inventory**
button to open a panel showing your carried items and equipment. Selecting an
item reveals its description with buttons to **Use** or **Drop** it directly
from the UI.
