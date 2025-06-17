import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from commands.consoles import engconsole_handler, cargoconsole_handler, secconsole_handler
from systems.power import PowerGrid
from systems import get_power_system, get_cargo_system, get_security_system


def test_engconsole_power_listing():
    ps = get_power_system()
    ps.grids.clear()
    grid = PowerGrid("g1", "Alpha")
    ps.register_grid(grid)
    result = engconsole_handler("test", action="power")
    assert "g1" in result


def test_cargoconsole_budgets():
    cargo = get_cargo_system()
    cargo.department_credits.clear()
    cargo.set_credits("engineering", 50)
    result = cargoconsole_handler("test", action="budgets")
    assert "engineering" in result


def test_secconsole_alerts():
    sec = get_security_system()
    sec.alerts.clear()
    sec.alerts.append({"type": "motion", "location": "hall"})
    result = secconsole_handler("test", action="alerts")
    assert "hall" in result
