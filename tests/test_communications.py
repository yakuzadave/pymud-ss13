import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.communications import CommunicationsSystem


def test_logs_and_encryption():
    system = CommunicationsSystem()
    system.register_channel("eng", "engineering")
    system.register_pda("pda1", "p1")
    system.register_pda("pda2", "p2")

    assert system.send_radio("p1", "eng", "hello")
    log = system.get_radio_log("eng")
    assert ("p1", "hello") in log

    key = system.generate_pda_key("pda2")
    assert key
    assert system.send_pda_message("pda1", "pda2", "secret", key=key)
    assert ("pda1", "secret") in system.get_pda_log("pda2")
    assert not system.send_pda_message("pda1", "pda2", "fail", key="bad")

    system.clear_radio_log("eng")
    system.clear_pda_log("pda2")
    assert system.get_radio_log("eng") == []
    assert system.get_pda_log("pda2") == []
