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


def test_fire_propagates_to_adjacent_tiles():
    grid = gs.AtmosGrid(2, 1)
    fire = FireSystem(grid)
    tile0 = grid.get_tile(0, 0)
    tile1 = grid.get_tile(1, 0)
    tile0.gas.composition["oxygen"] = 10.0
    tile1.gas.composition["oxygen"] = 10.0
    fire.ignite(0, 0, fuel=4, temperature=200.0)
    fire.step()
    assert any(src.tile is tile1 for src in fire.fires)
