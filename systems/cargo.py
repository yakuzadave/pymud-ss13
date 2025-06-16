"""Cargo and supply chain management system."""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from events import subscribe

logger = logging.getLogger(__name__)


@dataclass
class SupplyOrder:
    item: str
    quantity: int
    cost: int
    eta: float
    vendor: str
    department: str
    emergency: bool = False


class SupplyVendor:
    """Vendor with a dynamic catalog and limited stock."""

    def __init__(self, name: str, catalog: Optional[Dict[str, int]] = None) -> None:
        self.name = name
        self.catalog: Dict[str, int] = catalog or {}
        # Stock starts with a small quantity for each item
        self.stock: Dict[str, int] = {item: 10 for item in self.catalog}

    def get_price(self, item: str, demand: float = 1.0, shortage: bool = False) -> int:
        base = self.catalog.get(item, 0)
        price = int(base * demand)
        if shortage:
            price *= 2
        return max(price, 1)

    def has_stock(self, item: str, quantity: int) -> bool:
        return self.stock.get(item, 0) >= quantity

    def remove_stock(self, item: str, quantity: int) -> None:
        if item in self.stock:
            self.stock[item] = max(0, self.stock[item] - quantity)

    def restock(self, item: str, quantity: int) -> None:
        self.stock[item] = self.stock.get(item, 0) + quantity


class CargoSystem:
    """Central cargo and supply chain handler."""

    def __init__(self) -> None:
        self.vendors: Dict[str, SupplyVendor] = {}
        self.orders: List[SupplyOrder] = []
        self.inventory: Dict[str, Dict[str, int]] = {}
        self.market_demand: Dict[str, float] = {}
        self.department_credits: Dict[str, int] = {}
        # Track temporary supply shortages per item (remaining ticks)
        self.supply_shortages: Dict[str, int] = {}

        # Listen for economy-related events
        subscribe("market_event", self.apply_market_event)

    # ------------------------------------------------------------------
    def register_vendor(self, vendor: SupplyVendor) -> None:
        self.vendors[vendor.name] = vendor
        logger.debug("Registered vendor %s", vendor.name)

    # ------------------------------------------------------------------
    def set_credits(self, department: str, amount: int) -> None:
        """Set credit balance for a department."""
        self.department_credits[department] = max(amount, 0)

    def add_credits(self, department: str, amount: int) -> None:
        """Adjust credits by a positive or negative amount."""
        self.department_credits[department] = self.get_credits(department) + amount

    def get_credits(self, department: str) -> int:
        return self.department_credits.get(department, 0)

    # ------------------------------------------------------------------
    def order_supply(
        self,
        department: str,
        item: str,
        quantity: int,
        vendor: str,
        emergency: bool = False,
    ) -> Optional[SupplyOrder]:
        ven = self.vendors.get(vendor)
        if not ven:
            return None

        # Check for global or vendor shortages
        if self.supply_shortages.get(item, 0) > 0:
            logger.warning("%s is currently in shortage", item)
            return None
        if not ven.has_stock(item, quantity):
            logger.warning("Vendor %s lacks stock for %s", vendor, item)
            return None

        demand = self.market_demand.get(item, 1.0)
        cost = ven.get_price(item, demand) * quantity
        if self.get_credits(department) < cost:
            logger.warning(
                "%s lacks credits for order: %s x%d", department, item, quantity
            )
            return None
        self.department_credits[department] = self.get_credits(department) - cost
        eta = time.time() + (5 if emergency else 20)  # seconds until arrival
        order = SupplyOrder(item, quantity, cost, eta, vendor, department, emergency)
        self.orders.append(order)
        ven.remove_stock(item, quantity)
        logger.info(
            "Order placed for %s x%d from %s by %s", item, quantity, vendor, department
        )
        return order

    # ------------------------------------------------------------------
    def process_orders(self) -> None:
        now = time.time()
        arrived = [o for o in self.orders if o.eta <= now]
        self.orders = [o for o in self.orders if o.eta > now]
        for order in arrived:
            dept_inv = self.inventory.setdefault(order.vendor, {})
            dept_inv[order.item] = dept_inv.get(order.item, 0) + order.quantity
            logger.info("Order received for %s x%d", order.item, order.quantity)

    # ------------------------------------------------------------------
    def get_inventory(self, department: str) -> Dict[str, int]:
        return self.inventory.setdefault(department, {})

    # ------------------------------------------------------------------
    def set_market_demand(self, item: str, demand: float) -> None:
        self.market_demand[item] = max(demand, 0.1)

    # ------------------------------------------------------------------
    def update_economy(self) -> None:
        """Fluctuate market demand and resolve supply shortages."""
        for item, demand in list(self.market_demand.items()):
            delta = random.uniform(-0.2, 0.2)
            self.market_demand[item] = max(0.1, demand + delta)

        # Decrease shortage timers and restock when finished
        for item in list(self.supply_shortages.keys()):
            self.supply_shortages[item] -= 1
            if self.supply_shortages[item] <= 0:
                del self.supply_shortages[item]
                for ven in self.vendors.values():
                    if item in ven.catalog:
                        ven.restock(item, random.randint(5, 15))

        # Occasionally create a new shortage
        if self.market_demand and random.random() < 0.1:
            item = random.choice(list(self.market_demand.keys()))
            self.supply_shortages[item] = random.randint(2, 5)
            for ven in self.vendors.values():
                if item in ven.stock:
                    ven.stock[item] = 0
            logger.info("Supply shortage started for %s", item)

    # ------------------------------------------------------------------
    def apply_market_event(
        self, item: str, demand_delta: float = 0.0, shortage: Optional[int] = None
    ) -> None:
        """Handle external market events by adjusting demand or creating shortages."""
        if item:
            current = self.market_demand.get(item, 1.0)
            self.market_demand[item] = max(0.1, current + demand_delta)
            logger.info(
                "Market event changed demand for %s to %.2f", item, self.market_demand[item]
            )

        if shortage and shortage > 0:
            self.supply_shortages[item] = shortage
            for ven in self.vendors.values():
                if item in ven.stock:
                    ven.stock[item] = 0
            logger.info("Market event caused shortage of %s for %d ticks", item, shortage)

    # ------------------------------------------------------------------
    def transfer_supply(
        self,
        from_department: str,
        to_department: str,
        item: str,
        quantity: int,
        price: int,
    ) -> bool:
        """Move items between departments and handle credit exchange."""
        source = self.get_inventory(from_department)
        dest = self.get_inventory(to_department)
        if source.get(item, 0) < quantity:
            logger.warning("%s lacks %s x%d", from_department, item, quantity)
            return False
        total_cost = price * quantity
        if self.get_credits(to_department) < total_cost:
            logger.warning("%s cannot afford transfer cost", to_department)
            return False
        source[item] -= quantity
        dest[item] = dest.get(item, 0) + quantity
        self.add_credits(from_department, total_cost)
        self.add_credits(to_department, -total_cost)
        logger.info(
            "%s transferred %s x%d to %s for %d credits",
            from_department,
            item,
            quantity,
            to_department,
            total_cost,
        )
        return True


CARGO_SYSTEM = CargoSystem()


def get_cargo_system() -> CargoSystem:
    return CARGO_SYSTEM
