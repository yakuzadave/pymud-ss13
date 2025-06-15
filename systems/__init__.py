"""
Systems package for MUDpy SS13.
Systems handle game-wide mechanics like atmosphere and power.
Other systems manage jobs and random events.
"""

from .atmos import AtmosphericSystem, get_atmos_system
from .gas_sim import GasMixture, AtmosGrid, PipeNetwork
from .fire import FireSystem
from .power import PowerSystem, get_power_system
from .jobs import JobSystem, get_job_system
from .random_events import RandomEventSystem, get_random_event_system
from .antagonists import AntagonistSystem, get_antagonist_system
from .advanced_antagonists import (
    AdvancedAntagonistSystem,
    get_advanced_antagonist_system,
)
from .chemistry import ChemistrySystem, get_chemistry_system
from .disease import DiseaseSystem, get_disease_system
from .communications import CommunicationsSystem, get_comms_system
from .research import ResearchSystem, get_research_system
from .security import SecuritySystem, get_security_system
from .combat import CombatSystem, get_combat_system
from .communications import CommunicationsSystem, get_comms_system
from .cargo import CargoSystem, get_cargo_system
from .physics import PhysicsSystem, get_physics_system
from .maintenance import MaintenanceSystem, get_maintenance_system
from .genetics import GeneticsSystem, get_genetics_system
from .robotics import RoboticsSystem, get_robotics_system
from .botany import BotanySystem, get_botany_system
from .kitchen import KitchenSystem, get_kitchen_system
from .bar import BarSystem, get_bar_system
from .script_engine import ScriptEngine, get_script_engine
from .circuits import CircuitSystem, get_circuit_system
from .npc_ai import NPCSystem, get_npc_system
from .plumbing import PlumbingSystem, get_plumbing_system

__all__ = [
    "AtmosphericSystem",
    "get_atmos_system",
    "PowerSystem",
    "get_power_system",
    "JobSystem",
    "get_job_system",
    "RandomEventSystem",
    "get_random_event_system",
    "AntagonistSystem",
    "get_antagonist_system",
    "AdvancedAntagonistSystem",
    "get_advanced_antagonist_system",
    "ChemistrySystem",
    "get_chemistry_system",
    "DiseaseSystem",
    "get_disease_system",
    "ResearchSystem",
    "get_research_system",
    "SecuritySystem",
    "get_security_system",
    "CombatSystem",
    "get_combat_system",
    "CommunicationsSystem",
    "get_comms_system",
    "CargoSystem",
    "get_cargo_system",
    "PhysicsSystem",
    "get_physics_system",
    "MaintenanceSystem",
    "get_maintenance_system",
    "GeneticsSystem",
    "get_genetics_system",
    "RoboticsSystem",
    "get_robotics_system",
    "BotanySystem",
    "get_botany_system",
    "CircuitSystem",
    "get_circuit_system",
    "BarSystem",
    "get_bar_system",
    "KitchenSystem",
    "get_kitchen_system",
    "ScriptEngine",
    "get_script_engine",
    "GasMixture",
    "AtmosGrid",
    "PipeNetwork",
    "FireSystem",
    "NPCSystem",
    "get_npc_system",
    "PlumbingSystem",
    "get_plumbing_system",
]
