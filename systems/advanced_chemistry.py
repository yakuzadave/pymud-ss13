from dataclasses import dataclass, field
from typing import Dict, List, Optional

from systems.chemical_reactions import ChemicalContainerComponent


@dataclass
class ChemicalProperties:
    """Physical and chemical properties of a compound."""

    viscosity: float = 1.0
    solubility: float = 1.0
    reactivity: float = 1.0
    stability: float = 1.0  # higher means slower degradation


@dataclass
class Pharmacokinetics:
    """Basic drug metabolism parameters."""

    absorption_rate: float = 1.0
    half_life: float = 1.0  # hours
    metabolites: List[str] = field(default_factory=list)


@dataclass
class Compound:
    """Represents a complex chemical or drug."""

    name: str
    properties: ChemicalProperties = field(default_factory=ChemicalProperties)
    kinetics: Optional[Pharmacokinetics] = None
    purity: float = 1.0

    def degrade(self, hours: float) -> None:
        """Reduce purity over time based on stability."""
        if hours <= 0 or self.properties.stability <= 0:
            return
        loss = hours / self.properties.stability
        self.purity = max(0.0, self.purity - loss)

    def metabolize(self, hours: float) -> Dict[str, float]:
        """Simulate metabolism and return produced metabolites."""
        if not self.kinetics or hours <= 0:
            return {}
        fraction_remaining = 0.5 ** (hours / self.kinetics.half_life)
        produced = {}
        for met in self.kinetics.metabolites:
            produced[met] = (1 - fraction_remaining) * self.purity
        self.purity *= fraction_remaining
        return produced


@dataclass
class ReactionStep:
    """Single step in a multi-stage reaction."""

    inputs: List[str]
    output: str
    conditions: Dict[str, float] = field(default_factory=dict)


@dataclass
class ReactionChain:
    """Chain of reactions requiring intermediate compounds."""

    steps: List[ReactionStep] = field(default_factory=list)

    def process(
        self,
        available: Dict[str, float],
        container: ChemicalContainerComponent,
    ) -> List[str]:
        """Process the chain using reagents inside a container."""
        produced: List[str] = []
        for step in self.steps:
            if not all(available.get(inp, 0) > 0 for inp in step.inputs):
                continue
            if (
                "temperature" in step.conditions
                and container.temperature < step.conditions["temperature"]
            ):
                continue
            for inp in step.inputs:
                available[inp] -= 1
                if available[inp] <= 0:
                    del available[inp]
            available[step.output] = available.get(step.output, 0) + 1
            produced.append(step.output)
        return produced


@dataclass
class ChemicalEquipment:
    """Generic advanced chemical equipment."""

    name: str
    required_power: float = 0.0


@dataclass
class Centrifuge(ChemicalEquipment):
    """Device for refining compound purity."""

    def refine(self, compound: Compound) -> None:
        compound.purity = min(1.0, compound.purity + 0.1)


@dataclass
class Spectrometer(ChemicalEquipment):
    """Device for analysing chemical composition."""

    def analyze(self, compound: Compound) -> Dict[str, float]:
        return {
            "purity": compound.purity,
            "reactivity": compound.properties.reactivity,
        }


@dataclass
class ReactionChamber(ChemicalEquipment):
    """Enclosed vessel for controlled reactions."""

    capacity: float = 10.0


@dataclass
class QualityAssurance:
    """Quality control affecting potency and side effects."""

    def assess(self, compound: Compound) -> float:
        return compound.purity * compound.properties.reactivity


def check_safety(compound: Compound) -> bool:
    """Basic safety check based on reactivity."""
    return compound.properties.reactivity < 5
