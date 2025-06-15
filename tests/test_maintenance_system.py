import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import time
from components.maintenance import MaintainableComponent
from systems.maintenance import MaintenanceSystem


def test_equipment_degrades_and_fails():
    comp = MaintainableComponent(wear_rate=10.0, env_factor=1.0, failure_threshold=50)
    ms = MaintenanceSystem(tick_interval=0)
    ms.register("eq1", comp)
    ms.start()

    for _ in range(6):
        comp.apply_usage(intensity=1.0)
    assert comp.is_operational is False
    assert comp.condition <= 50

    repaired = comp.service(skill=1)
    assert repaired is True
    assert comp.is_operational is True
    assert comp.condition == 100.0


def test_maintenance_system_schedules_due():
    comp = MaintainableComponent(wear_rate=1.0)
    # Set due soon
    comp.next_service_due = time.time() - 1
    ms = MaintenanceSystem(tick_interval=0)
    ms.register("eq2", comp)
    ms.start()
    events = []

    def on_due(object_id: str):
        events.append(object_id)

    from events import subscribe

    subscribe("maintenance_due", on_due)
    ms.update()
    assert "eq2" in events
