from dataclasses import dataclass
from typing import List
from events import publish
from .gas_sim import AtmosGrid, AtmosTile

@dataclass
class FireSource:
    tile: AtmosTile
    fuel: float = 10.0
    temperature: float = 300.0

class FireSystem:
    def __init__(self, grid: AtmosGrid):
        self.grid = grid
        self.fires: List[FireSource] = []

    def ignite(self, x: int, y: int, fuel: float = 10.0, temperature: float = 300.0) -> None:
        tile = self.grid.get_tile(x, y)
        if tile:
            self.fires.append(FireSource(tile, fuel, temperature))
            publish("fire_started", x=x, y=y)

    def step(self) -> None:
        remaining: List[FireSource] = []
        for fire in self.fires:
            gas = fire.tile.gas
            burn = min(fire.fuel, gas.composition.get("oxygen", 0) / 5)
            if burn <= 0:
                continue
            gas.remove_gas("oxygen", burn * 5)
            gas.add_gas("co2", burn * 3)
            gas.add_gas("smoke", burn * 2)
            gas.temperature += burn * 2
            fire.fuel -= burn
            if fire.fuel > 0 and gas.composition.get("oxygen", 0) > 1:
                remaining.append(fire)
            else:
                publish("fire_extinguished", x=fire.tile.x, y=fire.tile.y)
        self.fires = remaining
