import systems.gas_sim as gs


def test_explosive_decompression_equalizes_pressure():
    grid = gs.AtmosGrid(2, 1)
    t1 = grid.get_tile(0, 0)
    t2 = grid.get_tile(1, 0)
    t1.gas.pressure = 150.0
    t2.gas.pressure = 50.0
    diff = grid.explosive_decompress((0, 0), (1, 0))
    assert diff == 100.0
    assert abs(t1.gas.pressure - t2.gas.pressure) < 0.01
