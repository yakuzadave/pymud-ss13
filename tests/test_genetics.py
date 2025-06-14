import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.genetics import GeneticsSystem


def test_basic_mutation_cycle():
    system = GeneticsSystem()
    profile = system.get_profile("p1")
    profile.add_gene("strength", 5)
    system.mutate_player("p1", "hulk", severity=1.0)
    assert "hulk" in profile.mutations
    system.tick()
    assert profile.instability < 1.0
    # stabilize fully
    system.stabilize_player("p1", amount=1.0)
    system.tick()
    assert profile.instability == 0.0
    assert profile.mutations == []


def test_dna_scanning():
    system = GeneticsSystem()
    p1 = system.get_profile("p1")
    p1.add_gene("strength", 5)
    system.mutate_player("p1", "hulk")
    system.scan_dna("p2", "p1")
    assert system.apply_scanned_dna("p2")
    p2 = system.get_profile("p2")
    assert p2.genes.get("strength") == 5
    assert "hulk" in p2.mutations

