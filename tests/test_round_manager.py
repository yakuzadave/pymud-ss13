import events
from systems.round_manager import RoundManager
from systems.antagonists import AntagonistSystem, Antagonist
from unittest import mock


def test_start_round_sets_mode(monkeypatch):
    antag = AntagonistSystem()
    manager = RoundManager(antag)

    mock_pub = mock.Mock()
    monkeypatch.setattr("systems.round_manager.publish", mock_pub)

    manager.start_round("traitor")
    assert manager.active is True
    assert manager.mode.name == "traitor"
    assert mock_pub.call_args_list[0].args[0] == "round_start"


def test_end_round_reports_winners(monkeypatch):
    antag = AntagonistSystem()
    antag.antagonists["p1"] = Antagonist("p1")
    antag.antagonists["p1"].completed = True

    manager = RoundManager(antag)
    monkeypatch.setattr("systems.round_manager.publish", lambda *a, **kw: None)

    manager.start_round("traitor")
    result = manager.end_round()
    assert result["winners"] == ["p1"]
    assert result["success"] is True
