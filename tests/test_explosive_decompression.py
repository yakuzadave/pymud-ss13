import systems.gas_sim as gs
from systems.hull_breach import HullBreachSystem


def test_explosive_decompression_equalizes_pressure():
    grid = gs.AtmosGrid(2, 1)
    t1 = grid.get_tile(0, 0)
    t2 = grid.get_tile(1, 0)
    t1.gas.pressure = 150.0
    t2.gas.pressure = 50.0
    diff = grid.explosive_decompress((0, 0), (1, 0))
    assert diff == 100.0
    assert abs(t1.gas.pressure - t2.gas.pressure) < 0.01


def test_hull_breach_system_decompresses_between_tiles():
    grid = gs.AtmosGrid(2, 1)
    hb = HullBreachSystem(grid)
    t1 = grid.get_tile(0, 0)
    t2 = grid.get_tile(1, 0)
    t1.gas.pressure = 130.0
    t2.gas.pressure = 70.0
    diff = hb.breach((0, 0), (1, 0))
    assert diff == 60.0
    assert abs(t1.gas.pressure - t2.gas.pressure) < 0.01
