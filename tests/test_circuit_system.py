import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.circuits import CircuitSystem
from components.circuit import CircuitComponent


def test_assemble_and_insert():
    system = CircuitSystem()
    system.add_parts("shell", 1)
    system.add_parts("board", 1)
    system.define_recipe("basic", "Compact Remote", {"shell": 1, "board": 1})
    circuit = system.assemble("c1", "basic")
    assert circuit is not None
    assert system.insert_component("c1", "button")
    assert circuit.components == ["button"]


def test_power_drain_and_auto_off():
    circuit = CircuitComponent(shell_type="Compact Remote", components=["a", "b"], power=3, active=True)
    system = CircuitSystem()
    system.circuits["c1"] = circuit
    system.tick()
    assert circuit.power == 1
    system.tick()
    assert circuit.power == 0
    assert circuit.active is False


def test_component_capacity():
    circuit = CircuitComponent(shell_type="Compact Remote")
    system = CircuitSystem()
    system.circuits["c1"] = circuit
    for i in range(30):
        system.insert_component("c1", f"c{i}")
    assert len(circuit.components) == circuit.max_components()
