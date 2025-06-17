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


def test_engconsole_usage():
    ps = get_power_system()
    ps.usage_history.clear()
    ps.usage_history["g1"] = [10, 20, 30]
    ps.grids["g1"] = PowerGrid("g1", "Alpha")
    result = engconsole_handler("test", action="usage", target="g1")
    assert "10" in result and "30" in result


def test_cargoconsole_route_management():
    cargo = get_cargo_system()
    cargo.shuttle_routes.clear()
    cargo.set_route("r1", ["A", "B"])
    out = cargoconsole_handler("test", action="route")
    assert "r1" in out and "A" in out


def test_secconsole_pardon():
    sec = get_security_system()
    sec.prisoners.clear()
    sec.prisoners["p1"] = sec.arrest("p1", duration=10)
    msg = secconsole_handler("test", action="pardon", target="p1")
    assert "released" in msg
    assert "p1" not in sec.prisoners
