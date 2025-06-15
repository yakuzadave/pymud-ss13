from systems.cargo import CargoSystem, SupplyVendor


def setup_system():
    system = CargoSystem()
    system.register_vendor(SupplyVendor("central", {"steel": 5}))
    system.set_credits("engineering", 20)
    return system


def test_order_deducts_credits():
    system = setup_system()
    order = system.order_supply("engineering", "steel", 2, "central")
    assert order is not None
    assert system.get_credits("engineering") == 10


def test_block_order_no_funds():
    system = setup_system()
    system.set_credits("engineering", 5)
    order = system.order_supply("engineering", "steel", 2, "central")
    assert order is None
    assert system.get_credits("engineering") == 5
