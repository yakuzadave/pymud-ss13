import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.communications import CommunicationsSystem


def test_encryption_and_logs():
    system = CommunicationsSystem()
    system.register_channel("eng", "engineering", encrypted=True, key="1234")
    system.register_pda("pda1", "p1")
    system.register_pda("pda2", "p2")

    assert not system.send_radio("p1", "eng", "hello", key="bad")
    assert system.send_radio("p1", "eng", "hello", key="1234")
    assert ("p1", "hello") in system.get_radio_log("eng")

    pkey = system.generate_pda_key("pda2")
    assert system.send_pda_message("pda1", "pda2", "secret", key=pkey)
    assert system.get_pda_file_log("pda2") == []
    assert ("pda1", "secret") in system.get_pda_log("pda2")
    system.send_pda_message("pda1", "pda2", "file", file="report.txt", key=pkey)
    assert ("pda1", "report.txt") in system.get_pda_file_log("pda2")


def test_jamming_and_private_messages():
    system = CommunicationsSystem()
    system.register_channel("ops", "operations")
    system.register_pda("pda1", "p1")
    system.register_pda("pda2", "p2")

    system.jam_channel("ops")
    assert not system.send_radio("p1", "ops", "test")
    system.unjam_channel("ops")
    assert system.send_radio("p1", "ops", "test")

    key = system.generate_private_key("p2")
    assert not system.send_private_message("p1", "p2", "hi", key="bad")
    assert system.send_private_message("p1", "p2", "hi", key=key)
    assert ("p1", "hi") in system.get_private_log("p2")
    system.jam_private_messages()
    assert not system.send_private_message("p1", "p2", "blocked", key=key)
    system.unjam_private_messages()
    assert system.send_private_message("p1", "p2", "ok", key=key)
