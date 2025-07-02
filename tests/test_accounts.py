import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import account_system as accounts
from pathlib import Path


def test_account_creation_and_auth(monkeypatch, tmp_path):
    acc_file = tmp_path / "accounts.yaml"
    monkeypatch.setattr(accounts, "ACCOUNTS_FILE", acc_file)
    accounts.create_account("bob", "pass")
    assert accounts.authenticate("bob", "pass")
    assert not accounts.authenticate("bob", "wrong")


def test_admin_flag(monkeypatch, tmp_path):
    acc_file = tmp_path / "accounts.yaml"
    monkeypatch.setattr(accounts, "ACCOUNTS_FILE", acc_file)
    accounts.create_account("root", "pw", admin=True)
    assert accounts.is_admin("root")
    assert not accounts.is_admin("other")


def test_character_storage(monkeypatch, tmp_path):
    acc_file = tmp_path / "accounts.yaml"
    monkeypatch.setattr(accounts, "ACCOUNTS_FILE", acc_file)
    accounts.create_account("alice", "pw")
    assert accounts.get_character("alice") is None
    accounts.set_character("alice", {"job": "doctor", "name": "Dr Alice"})
    data = accounts.get_character("alice")
    assert data["job"] == "doctor"
    assert data["name"] == "Dr Alice"
