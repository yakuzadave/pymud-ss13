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

    def ignite(
        self, x: int, y: int, fuel: float = 10.0, temperature: float = 300.0
    ) -> None:
        tile = self.grid.get_tile(x, y)
        if tile:
            tile.gas.temperature = max(tile.gas.temperature, temperature)
            self.fires.append(FireSource(tile, fuel, temperature))
            publish("fire_started", x=x, y=y)

    def step(self) -> None:
        remaining: List[FireSource] = []
        new_fires: List[FireSource] = []
        active_tiles = {(f.tile.x, f.tile.y) for f in self.fires}
        added_tiles = set()
        for fire in self.fires:
            gas = fire.tile.gas
            burn = min(fire.fuel, gas.composition.get("oxygen", 0) / 5)
            if burn <= 0:
                continue
            gas.remove_gas("oxygen", burn * 5)
            gas.add_gas("co2", burn * 3)
            gas.add_gas("smoke", burn * 2)
            fire.temperature += burn * 2
            gas.temperature = max(gas.temperature, fire.temperature)
            fire.fuel -= burn
            if fire.temperature > 150 and fire.fuel > 1:
                for nbr in self.grid.neighbours(fire.tile):
                    coord = (nbr.x, nbr.y)
                    if coord not in active_tiles and coord not in added_tiles:
                        if nbr.gas.composition.get("oxygen", 0) > 5:
                            new_fires.append(
                                FireSource(nbr, fuel=fire.fuel / 2, temperature=fire.temperature)
                            )
                            added_tiles.add(coord)
                            publish("fire_started", x=nbr.x, y=nbr.y)

            if fire.fuel > 0 and gas.composition.get("oxygen", 0) > 1:
                remaining.append(fire)
            else:
                publish("fire_extinguished", x=fire.tile.x, y=fire.tile.y)
        self.fires = remaining + new_fires
