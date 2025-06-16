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


def test_market_update_changes_demand():
    system = setup_system()
    system.set_market_demand("steel", 1.0)
    before = system.market_demand["steel"]
    system.update_economy()
    after = system.market_demand["steel"]
    assert before != after


def test_shortage_blocks_order():
    system = setup_system()
    system.supply_shortages["steel"] = 2
    order = system.order_supply("engineering", "steel", 1, "central")
    assert order is None


def test_market_event_adjusts_demand():
    system = setup_system()
    system.set_market_demand("steel", 1.0)
    system.apply_market_event(item="steel", demand_delta=2.0)
    assert system.market_demand["steel"] == 3.0


def test_transfer_supply_moves_items_and_credits():
    system = setup_system()
    system.get_inventory("mining")["ore"] = 5
    system.set_credits("mining", 0)
    system.set_credits("engineering", 20)
    transferred = system.transfer_supply("mining", "engineering", "ore", 2, 3)
    assert transferred
    assert system.get_inventory("mining").get("ore") == 3
    assert system.get_inventory("engineering").get("ore") == 2
    assert system.get_credits("mining") == 6
    assert system.get_credits("engineering") == 14
