import logging
from typing import Dict, List, Tuple, Optional

import world
from events import publish

logger = logging.getLogger(__name__)


class SurgerySystem:
    """Manage surgical procedures with skill checks and required equipment."""

    def __init__(self) -> None:
        self.procedures: Dict[str, Dict] = {
            "appendectomy": {
                "steps": ["incision", "remove_appendix", "suture"],
                "required_skill": 2,
                "required_tools": ["scalpel", "suture_kit"],
                "healing": [("torso", "brute", 20)],
            },
            "antiviral": {
                "steps": ["incision", "administer_antiviral", "suture"],
                "required_skill": 1,
                "required_tools": ["scalpel", "suture_kit"],
                "healing": [],
                "cures": ["virus_x"],
            },
        }
        self.active: Dict[Tuple[str, str], Dict] = {}

    def start_procedure(self, surgeon_id: str, patient_id: str, procedure: str) -> bool:
        """Begin a surgery if skill and tools allow."""
        data = self.procedures.get(procedure)
        if not data:
            return False
        world_instance = world.get_world()
        surgeon = world_instance.get_object(surgeon_id)
        patient = world_instance.get_object(patient_id)
        if not surgeon or not patient:
            return False
        s_comp = surgeon.get_component("player")
        p_comp = patient.get_component("player")
        if not s_comp or not p_comp:
            return False
        level = s_comp.skills.get("surgery", 0)
        if level < data.get("required_skill", 0):
            return False
        for tool in data.get("required_tools", []):
            if tool not in s_comp.inventory:
                return False
        self.active[(surgeon_id, patient_id)] = {
            "procedure": procedure,
            "step": 0,
        }
        publish(
            "surgery_started",
            surgeon_id=surgeon_id,
            patient_id=patient_id,
            procedure=procedure,
        )
        return True

    def perform_step(self, surgeon_id: str, patient_id: str) -> Optional[str]:
        key = (surgeon_id, patient_id)
        info = self.active.get(key)
        if not info:
            return None
        data = self.procedures.get(info["procedure"])
        if not data:
            return None
        step_idx = info["step"]
        steps = data.get("steps", [])
        if step_idx >= len(steps):
            return None
        step = steps[step_idx]
        info["step"] += 1
        if info["step"] >= len(steps):
            # completed
            world_instance = world.get_world()
            patient = world_instance.get_object(patient_id)
            if patient:
                p_comp = patient.get_component("player")
                if p_comp:
                    for part, dtype, amt in data.get("healing", []):
                        p_comp.heal_damage(part, dtype, amt)
                    for disease in data.get("cures", []):
                        p_comp.cure_disease(disease)
            publish(
                "surgery_completed",
                surgeon_id=surgeon_id,
                patient_id=patient_id,
                procedure=info["procedure"],
            )
            del self.active[key]
        return step


SURGERY_SYSTEM = SurgerySystem()


def get_surgery_system() -> SurgerySystem:
    return SURGERY_SYSTEM
