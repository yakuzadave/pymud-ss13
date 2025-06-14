from systems.advanced_chemistry import (
    ReactionStep,
    ReactionChain,
    ChemicalProperties,
    Pharmacokinetics,
    Compound,
)
from systems.chemical_reactions import ChemicalContainerComponent


def test_multi_step_reaction_chain():
    chain = ReactionChain(
        steps=[
            ReactionStep(inputs=["chemical_a", "chemical_b"], output="intermediate"),
            ReactionStep(inputs=["intermediate", "chemical_c"], output="final"),
        ]
    )
    container = ChemicalContainerComponent(capacity=5)
    available = {"chemical_a": 1, "chemical_b": 1, "chemical_c": 1}
    result = chain.process(available, container)
    assert result == ["intermediate", "final"]
    assert available.get("final") == 1


def test_pharmacokinetics_metabolism():
    props = ChemicalProperties(stability=10.0)
    kinetics = Pharmacokinetics(half_life=1.0, metabolites=["metabolite"])
    drug = Compound(name="drug_x", properties=props, kinetics=kinetics)
    out = drug.metabolize(1.0)
    assert out.get("metabolite")
    assert drug.purity < 1.0
