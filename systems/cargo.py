"""Cargo and supply chain management system."""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

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
    """Vendor with a dynamic catalog."""

    def __init__(self, name: str, catalog: Optional[Dict[str, int]] = None) -> None:
        self.name = name
        self.catalog: Dict[str, int] = catalog or {}

    def get_price(self, item: str, demand: float = 1.0) -> int:
        base = self.catalog.get(item, 0)
        # Very small pricing algorithm
        price = int(base * demand)
        return max(price, 1)


class CargoSystem:
    """Central cargo and supply chain handler."""

    def __init__(self) -> None:
        self.vendors: Dict[str, SupplyVendor] = {}
        self.orders: List[SupplyOrder] = []
        self.inventory: Dict[str, Dict[str, int]] = {}
        self.market_demand: Dict[str, float] = {}
        self.department_credits: Dict[str, int] = {}

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


CARGO_SYSTEM = CargoSystem()


def get_cargo_system() -> CargoSystem:
    return CARGO_SYSTEM
