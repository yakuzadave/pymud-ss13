import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.security import SecuritySystem


def test_report_and_arrest():
    sec = SecuritySystem()
    rec = sec.report_crime("player_1", "Stole tools", suspect_id="player_2")
    assert rec.crime_id == 1
    assert rec.suspect_id == "player_2"

    prisoner = sec.arrest("player_2", duration=1)
    assert prisoner.player_id == "player_2"
    assert "player_2" in sec.prisoners

    time.sleep(1.1)
    sec.check_sentence_expirations()
    assert "player_2" not in sec.prisoners
