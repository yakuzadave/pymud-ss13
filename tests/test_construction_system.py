import sys
import os
import random

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.construction import (
    ConstructionSystem,
    ConstructionProject,
    ConstructionStage,
)


def test_project_completes_with_multiple_stages():
    system = ConstructionSystem()
    stages = [
        ConstructionStage("foundation", "engineer", duration=2, resources={"steel": 5}),
        ConstructionStage("wiring", "electrician", duration=1, resources={"cable": 2}),
    ]
    project = ConstructionProject("p1", "Generator", stages)
    system.add_project(project)
    system.assign_worker("p1", "w1", "engineer")
    system.assign_worker("p1", "w2", "electrician")
    system.add_resources("p1", {"steel": 5, "cable": 2})

    for _ in range(3):
        system.update()

    assert project.is_completed()
    assert project.quality_score == 100


def test_safety_officer_prevents_accidents(monkeypatch):
    random.seed(1)
    system = ConstructionSystem()
    stage = ConstructionStage(
        "high_voltage",
        "electrician",
        duration=1,
        resources={},
        hazard_level=1.0,
    )
    project = ConstructionProject("p2", "Dangerous", [stage])
    system.add_project(project)
    system.assign_worker("p2", "e1", "electrician")

    # Without safety officer an accident should occur
    system.update()
    assert project.is_completed()
    assert project.quality_score < 100

    # Now try with a safety officer to avoid accident
    stage2 = ConstructionStage(
        "safe_stage",
        "engineer",
        duration=1,
        resources={},
        hazard_level=1.0,
    )
    project2 = ConstructionProject("p3", "Safe", [stage2])
    system.add_project(project2)
    system.assign_worker("p3", "e2", "engineer")
    system.assign_worker("p3", "s1", "safety_officer")
    system.update()
    assert project2.is_completed()
    assert project2.quality_score == 100

