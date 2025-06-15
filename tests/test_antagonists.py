import events
from systems.antagonists import AntagonistSystem
from unittest import mock


def test_assign_and_remove_antagonist(monkeypatch):
    system = AntagonistSystem()

    mock_pub = mock.Mock()
    monkeypatch.setattr(events, "publish", mock_pub)
    import systems.antagonists as sa

    monkeypatch.setattr(sa, "publish", mock_pub)

    antag = system.assign_antagonist("p1", objectives=["steal"], gear=["kit"])
    assert antag.player_id == "p1"
    assert antag.objectives == ["steal"]
    assert mock_pub.call_args_list[0].args[0] == "antagonist_assigned"

    assert system.remove_antagonist("p1") is True
    assert mock_pub.call_args_list[-1].args[0] == "antagonist_removed"


def test_choose_random_antagonists(monkeypatch):
    system = AntagonistSystem()
    monkeypatch.setattr("random.sample", lambda seq, k: seq[:k])

    chosen = system.choose_random_antagonists(["a", "b", "c"], count=2)
    assert set(chosen) == {"a", "b"}
    assert len(system.list_antagonists()) == 2
