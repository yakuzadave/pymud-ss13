"""Research and Development system for MUDpy SS13.

This module implements a simplified technology research framework. It allows
departments to accumulate research points, unlock technologies and build
prototypes once the required research is completed. The implementation is kept
lightweight so that tests can exercise basic functionality without needing a
full in game integration yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


@dataclass
class ResearchTechnology:
    """Represents a technology in the research tree."""

    tech_id: str
    name: str
    description: str = ""
    prerequisites: List[str] = field(default_factory=list)
    department: Optional[str] = None
    points_required: int = 0
    prototype_ids: List[str] = field(default_factory=list)
    obsolete_by: Optional[str] = None
    upgrades: List[str] = field(default_factory=list)


@dataclass
class Prototype:
    """Prototype unlocked by researching a technology."""

    proto_id: str
    name: str
    technology: str
    required_materials: List[str] = field(default_factory=list)
    required_equipment: List[str] = field(default_factory=list)
    object_id: Optional[str] = None


class ResearchSystem:
    """Main research system managing technologies and prototypes."""

    def __init__(self) -> None:
        self.technologies: Dict[str, ResearchTechnology] = {}
        self.prototypes: Dict[str, Prototype] = {}
        self.research_points: Dict[str, int] = {}
        self.completed: Set[str] = set()
        self.owners: Dict[str, Set[str]] = {}
        self.unlocked_blueprints: Set[str] = set()
        logger.info("Research system initialized")

    # -- Technology registration -------------------------------------------------
    def register_technology(self, tech: ResearchTechnology) -> None:
        self.technologies[tech.tech_id] = tech
        logger.debug("Registered technology %s", tech.tech_id)

    def register_prototype(self, proto: Prototype) -> None:
        self.prototypes[proto.proto_id] = proto
        if proto.technology in self.technologies:
            self.technologies[proto.technology].prototype_ids.append(proto.proto_id)
        logger.debug("Registered prototype %s", proto.proto_id)

    # -- Research points ---------------------------------------------------------
    def add_points(self, department: str, points: int) -> None:
        self.research_points[department] = (
            self.research_points.get(department, 0) + points
        )
        logger.debug("Added %s research points to %s", points, department)

    def get_points(self, department: str) -> int:
        return self.research_points.get(department, 0)

    # -- Research progression ----------------------------------------------------
    def _requirements_met(self, tech: ResearchTechnology, dept: str) -> bool:
        if self.get_points(dept) < tech.points_required:
            return False
        for prereq in tech.prerequisites:
            if prereq not in self.completed:
                return False
        return True

    def research(self, department: str, tech_id: str) -> bool:
        tech = self.technologies.get(tech_id)
        if not tech or tech_id in self.completed:
            return False
        if not self._requirements_met(tech, department):
            return False
        self.research_points[department] -= tech.points_required
        self.completed.add(tech_id)
        self.owners.setdefault(department, set()).add(tech_id)
        for pid in tech.prototype_ids:
            self.unlocked_blueprints.add(pid)
        logger.info("Department %s completed research: %s", department, tech_id)
        return True

    def has_technology(self, department: str, tech_id: str) -> bool:
        return tech_id in self.owners.get(department, set())

    # -- Prototype construction --------------------------------------------------
    def build_prototype(
        self,
        department: str,
        proto_id: str,
        materials: List[str],
        equipment: List[str],
    ) -> bool:
        proto = self.prototypes.get(proto_id)
        if not proto:
            return False
        if proto_id not in self.unlocked_blueprints:
            return False
        if not self.has_technology(department, proto.technology):
            return False
        if any(req not in materials for req in proto.required_materials):
            return False
        if any(req not in equipment for req in proto.required_equipment):
            return False
        if proto.object_id:
            self._spawn_object(proto.object_id)
        logger.info("%s successfully built prototype %s", department, proto_id)
        return True

    # -- Technology transfer -----------------------------------------------------
    def transfer_technology(self, tech_id: str, from_dept: str, to_dept: str) -> bool:
        if tech_id not in self.owners.get(from_dept, set()):
            return False
        self.owners.setdefault(to_dept, set()).add(tech_id)
        logger.info("Transferred %s from %s to %s", tech_id, from_dept, to_dept)
        return True

    # -- Obsolescence ------------------------------------------------------------
    def is_obsolete(self, tech_id: str) -> bool:
        tech = self.technologies.get(tech_id)
        return bool(tech and tech.obsolete_by and tech.obsolete_by in self.completed)

    # -- Object spawning -------------------------------------------------------
    def _spawn_object(self, object_id: str) -> None:
        """Spawn an object from the objects data file."""
        from world import get_world, GameObject
        from components import COMPONENT_REGISTRY
        import yaml, os, inspect

        path = os.path.join("data", "objects.yaml")
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f) or []
        except Exception:
            return
        for obj_data in data:
            if obj_data.get("id") != object_id:
                continue
            obj = GameObject(
                id=obj_data["id"],
                name=obj_data.get("name", object_id),
                description=obj_data.get("description", ""),
                location=obj_data.get("location"),
            )
            comps = obj_data.get("components", {})
            for comp_name, comp_data in comps.items():
                comp_class = COMPONENT_REGISTRY.get(comp_name)
                if comp_class and isinstance(comp_data, dict):
                    params = inspect.signature(comp_class.__init__).parameters
                    kwargs = {k: v for k, v in comp_data.items() if k in params and k != "self"}
                    try:
                        comp_instance = comp_class(**kwargs)
                    except Exception:
                        continue
                    obj.add_component(comp_name, comp_instance)
                else:
                    obj.components[comp_name] = comp_data
            get_world().register(obj)
            break


# Create global instance
RESEARCH_SYSTEM = ResearchSystem()


def get_research_system() -> ResearchSystem:
    return RESEARCH_SYSTEM
