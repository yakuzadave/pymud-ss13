import systems.gas_sim as gs
from systems.fire import FireSystem


def test_fire_consumes_oxygen_and_produces_smoke():
    grid = gs.AtmosGrid(1, 1)
    fire = FireSystem(grid)
    tile = grid.get_tile(0, 0)
    tile.gas.composition["oxygen"] = 10.0
    fire.ignite(0, 0, fuel=2)
    fire.step()
    assert tile.gas.composition["oxygen"] < 10.0
    assert tile.gas.composition["smoke"] > 0.0
