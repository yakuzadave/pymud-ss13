from systems.cargo import CargoSystem, SupplyVendor
import time


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


def test_market_event_subscription_boom():
    from events import publish

    system = setup_system()
    system.set_market_demand("steel", 1.0)
    publish("market_boom", item="steel", demand_delta=1.0)
    assert system.market_demand["steel"] == 2.0


def test_market_event_shortage_sets_stock():
    system = setup_system()
    ven = system.vendors["central"]
    ven.stock["steel"] = 5
    system.apply_market_event(item="steel", shortage=2)
    assert system.supply_shortages["steel"] == 2
    assert ven.stock["steel"] == 0


def test_order_delivery_updates_inventory():
    system = setup_system()
    order = system.order_supply("engineering", "steel", 1, "central")
    assert order is not None
    order.eta = time.time() - 1
    system.process_orders()
    assert system.get_inventory("engineering").get("steel") == 1


def test_trade_command_transfers_goods(monkeypatch):
    from commands import cargo as cmd_cargo

    system = setup_system()
    system.get_inventory("mining")["ore"] = 5
    system.set_credits("mining", 0)
    system.set_credits("engineering", 20)
    monkeypatch.setattr(cmd_cargo, "get_cargo_system", lambda: system)
    out = cmd_cargo.trade_handler(None, "1", "mining engineering ore 2 3")
    assert "Transferred" in out
    assert system.get_inventory("mining").get("ore") == 3
    assert system.get_inventory("engineering").get("ore") == 2
    assert system.get_credits("mining") == 6
    assert system.get_credits("engineering") == 14
