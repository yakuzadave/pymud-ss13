import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.plumbing import PlumbingSystem
from components.fluid import FluidContainerComponent


def test_fluid_moves_between_devices():
    system = PlumbingSystem(tick_interval=0)
    src = FluidContainerComponent(capacity=10)
    dst = FluidContainerComponent(capacity=5)
    src.add_fluid("water", 5)

    system.register_device("tank", src)
    system.register_device("tray", dst)
    system.connect("tank", "tray")
    system.start()
    system.update()

    assert dst.contents.get("water") == 5
    assert src.current_volume() == 0


def test_transfer_respects_capacity():
    system = PlumbingSystem(tick_interval=0)
    src = FluidContainerComponent(capacity=10)
    dst = FluidContainerComponent(capacity=3)
    src.add_fluid("nutrient", 5)

    system.register_device("tank", src)
    system.register_device("tray", dst)
    system.connect("tank", "tray")
    system.start()
    system.update()

    assert dst.current_volume() == 3
    assert src.current_volume() == 2
