from systems.chemical_reactions import (
    ChemicalReactionSystem,
    ChemicalContainerComponent,
    Reagent,
    Reaction,
)


def setup_system() -> ChemicalReactionSystem:
    system = ChemicalReactionSystem()
    system.register_reagent(Reagent("water"))
    system.register_reagent(Reagent("sodium"))
    system.register_reagent(Reagent("explosive"))
    system.add_reaction(
        Reaction(reactants=["water", "sodium"], products=["explosive"], min_temp=50)
    )
    return system


def test_reaction_requires_temperature():
    system = setup_system()
    container = ChemicalContainerComponent(capacity=5, temperature=20)
    container.add_reagent("water", 1)
    container.add_reagent("sodium", 1)

    # reaction should not occur below minimum temperature
    result = system.process_container(container)
    assert result == []
    assert "explosive" not in container.contents

    container.heat(60)
    result = system.process_container(container)
    assert result == ["explosive"]
    assert container.contents.get("explosive") == 1
    assert "water" not in container.contents
    assert "sodium" not in container.contents


def test_container_mixing_and_reaction():
    system = setup_system()
    a = ChemicalContainerComponent(capacity=5)
    b = ChemicalContainerComponent(capacity=5)
    a.add_reagent("water", 1)
    b.add_reagent("sodium", 1)

    a.transfer_to(b)
    assert "water" in b.contents and "sodium" in b.contents

    b.heat(60)
    result = system.process_container(b)
    assert result == ["explosive"]
    assert "explosive" in b.contents
