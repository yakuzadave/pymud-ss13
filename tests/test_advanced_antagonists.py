import events
from systems.advanced_antagonists import AdvancedAntagonistSystem
from unittest import mock


def test_cult_conversion_and_ritual(monkeypatch):
    system = AdvancedAntagonistSystem()

    mock_pub = mock.Mock()
    monkeypatch.setattr(events, "publish", mock_pub)
    import systems.advanced_antagonists as aa
    monkeypatch.setattr(aa, "publish", mock_pub)

    cult = system.create_cult("blood", "p1")
    system.convert_to_cult("blood", "p2")
    assert "p2" in cult.members

    ok = cult.perform_ritual("summon", {"p1", "p2"})
    assert ok is True


def test_changeling_absorb_identity(monkeypatch):
    system = AdvancedAntagonistSystem()

    mock_pub = mock.Mock()
    monkeypatch.setattr(events, "publish", mock_pub)
    import systems.advanced_antagonists as aa
    monkeypatch.setattr(aa, "publish", mock_pub)

    ling = system.spawn_changeling("c1")
    ling.absorb_identity("t1", "dna")
    assert "t1" in ling.absorbed_dna


def test_revolutionary_recruitment():
    system = AdvancedAntagonistSystem()
    cell = system.create_cell("r1")
    cell.recruit("p3")
    assert "p3" in cell.members


def test_gang_territory():
    system = AdvancedAntagonistSystem()
    gang = system.create_gang("sharks")
    gang.claim_territory("sec")
    assert "sec" in gang.territory


def test_sleeper_activation():
    system = AdvancedAntagonistSystem()
    agent = system.assign_sleeper("s1", mission="watch")
    agent.activate()
    assert agent.activated is True


def test_dynamic_role_generation(monkeypatch):
    system = AdvancedAntagonistSystem()
    monkeypatch.setattr("random.choice", lambda seq: seq[0])
    role = system.generate_antagonist_role("p9")
    assert role in {"cultist", "changeling", "revolutionary", "gangster", "sleeper"}

