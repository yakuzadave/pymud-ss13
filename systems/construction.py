"""Construction system for managing complex engineering projects."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class ConstructionStage:
    """A single stage within a construction project."""

    name: str
    required_role: str
    duration: int
    resources: Dict[str, int] = field(default_factory=dict)
    hazard_level: float = 0.0  # 0-1 chance of accident without safety officer
    completed: bool = False
    progress: int = 0


class ConstructionProject:
    """Represents a multi-stage construction project."""

    def __init__(
        self,
        project_id: str,
        name: str,
        stages: List[ConstructionStage],
        category: str = "generic",
        quality_target: int = 100,
    ) -> None:
        self.project_id = project_id
        self.name = name
        self.stages = stages
        self.category = category
        self.quality_target = quality_target
        self.quality_score = quality_target
        self.current_stage_idx = 0
        self.assigned_workers: Dict[str, str] = {}
        self.resources: Dict[str, int] = {}
        self.completed = False

    # ------------------------------------------------------------------
    # Worker and resource management
    # ------------------------------------------------------------------
    def assign_worker(self, worker_id: str, role: str) -> None:
        self.assigned_workers[worker_id] = role

    def unassign_worker(self, worker_id: str) -> None:
        self.assigned_workers.pop(worker_id, None)

    def add_resources(self, resources: Dict[str, int]) -> None:
        for name, amt in resources.items():
            self.resources[name] = self.resources.get(name, 0) + amt

    def _has_required_resources(self, stage: ConstructionStage) -> bool:
        for name, amt in stage.resources.items():
            if self.resources.get(name, 0) < amt:
                return False
        return True

    def _consume_resources(self, stage: ConstructionStage) -> None:
        for name, amt in stage.resources.items():
            self.resources[name] = self.resources.get(name, 0) - amt

    def _has_worker_role(self, role: str) -> bool:
        return role in self.assigned_workers.values()

    def _has_safety_officer(self) -> bool:
        return self._has_worker_role("safety_officer")

    # ------------------------------------------------------------------
    # Progress handling
    # ------------------------------------------------------------------
    def current_stage(self) -> Optional[ConstructionStage]:
        if self.current_stage_idx >= len(self.stages):
            return None
        return self.stages[self.current_stage_idx]

    def advance(self) -> None:
        if self.completed:
            return

        stage = self.current_stage()
        if stage is None:
            return

        if not self._has_worker_role(stage.required_role):
            return
        if not self._has_required_resources(stage):
            return

        stage.progress += 1
        logger.debug(
            f"Project {self.project_id} advancing stage {stage.name}: {stage.progress}/{stage.duration}"
        )

        if stage.progress >= stage.duration:
            stage.completed = True
            self._consume_resources(stage)
            publish(
                "stage_completed",
                project_id=self.project_id,
                stage=stage.name,
            )

            # Safety check
            if stage.hazard_level > 0 and not self._has_safety_officer():
                if random.random() < stage.hazard_level:
                    self.quality_score -= 20
                    publish(
                        "construction_accident",
                        project_id=self.project_id,
                        stage=stage.name,
                    )

            self.current_stage_idx += 1
            if self.current_stage_idx >= len(self.stages):
                self.completed = True
                publish(
                    "project_completed",
                    project_id=self.project_id,
                    quality=self.quality_score,
                    category=self.category,
                )
                return
            else:
                publish(
                    "stage_started",
                    project_id=self.project_id,
                    stage=self.stages[self.current_stage_idx].name,
                )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def is_completed(self) -> bool:
        return self.completed


class ConstructionSystem:
    """Manages construction projects and progress."""

    def __init__(self) -> None:
        self.projects: Dict[str, ConstructionProject] = {}

    def add_project(self, project: ConstructionProject) -> None:
        self.projects[project.project_id] = project
        publish("project_started", project_id=project.project_id, name=project.name)

    def assign_worker(self, project_id: str, worker_id: str, role: str) -> None:
        if project_id in self.projects:
            self.projects[project_id].assign_worker(worker_id, role)

    def add_resources(self, project_id: str, resources: Dict[str, int]) -> None:
        if project_id in self.projects:
            self.projects[project_id].add_resources(resources)

    def update(self) -> None:
        for project in list(self.projects.values()):
            project.advance()


CONSTRUCTION_SYSTEM = ConstructionSystem()


def get_construction_system() -> ConstructionSystem:
    """Return the global construction system."""

    return CONSTRUCTION_SYSTEM

