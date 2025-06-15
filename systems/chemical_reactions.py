from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Reagent:
    """Represents a chemical reagent with basic properties."""

    name: str
    toxicity: float = 0.0
    ph: float = 7.0
    temperature_effects: Dict[str, float] = field(default_factory=dict)


@dataclass
class Reaction:
    """Defines a chemical reaction."""

    reactants: List[str]
    products: List[str]
    byproducts: List[str] = field(default_factory=list)
    min_temp: Optional[float] = None
    catalyst: Optional[str] = None


class ChemicalContainerComponent:
    """Container capable of holding chemical reagents."""

    def __init__(
        self,
        capacity: float = 100.0,
        container_type: str = "beaker",
        temperature: float = 20.0,
    ):
        self.owner = None
        self.capacity = capacity
        self.container_type = container_type
        self.temperature = temperature
        self.contents: Dict[str, float] = {}

    def current_volume(self) -> float:
        return sum(self.contents.values())

    def add_reagent(self, name: str, amount: float = 1.0) -> bool:
        if self.current_volume() + amount > self.capacity:
            return False
        self.contents[name] = self.contents.get(name, 0.0) + amount
        return True

    def remove_reagent(self, name: str, amount: float = 1.0) -> bool:
        if self.contents.get(name, 0.0) < amount:
            return False
        self.contents[name] -= amount
        if self.contents[name] <= 0:
            del self.contents[name]
        return True

    def heat(self, temperature: float) -> None:
        self.temperature = temperature

    def transfer_to(self, other: "ChemicalContainerComponent") -> None:
        for name, amount in list(self.contents.items()):
            if other.add_reagent(name, amount):
                self.remove_reagent(name, amount)


class ChemicalReactionSystem:
    """Processes chemical reactions inside containers."""

    def __init__(self):
        self.reagents: Dict[str, Reagent] = {}
        self.reactions: List[Reaction] = []

    def register_reagent(self, reagent: Reagent) -> None:
        self.reagents[reagent.name] = reagent

    def add_reaction(self, reaction: Reaction) -> None:
        self.reactions.append(reaction)

    def process_container(self, container: ChemicalContainerComponent) -> List[str]:
        """Check container and apply any matching reactions."""
        results = []
        for reaction in self.reactions:
            if reaction.catalyst and reaction.catalyst not in container.contents:
                continue
            if (
                reaction.min_temp is not None
                and container.temperature < reaction.min_temp
            ):
                continue
            if all(r in container.contents for r in reaction.reactants):
                for r in reaction.reactants:
                    container.remove_reagent(r)
                for p in reaction.products:
                    container.add_reagent(p)
                for b in reaction.byproducts:
                    container.add_reagent(b)
                results.append("+".join(reaction.products))
        return results
