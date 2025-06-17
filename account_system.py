import yaml
from pathlib import Path
import os
import hashlib
from typing import Dict

ACCOUNTS_FILE = Path('data/accounts.yaml')


def _load() -> Dict[str, dict]:
    if ACCOUNTS_FILE.exists():
        with open(ACCOUNTS_FILE, 'r') as f:
            data = yaml.safe_load(f) or {}
            if isinstance(data, dict):
                return data
    return {}


def _save(data: Dict[str, dict]) -> None:
    ACCOUNTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ACCOUNTS_FILE, 'w') as f:
        yaml.safe_dump(data, f)


def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()


def create_account(username: str, password: str, admin: bool = False) -> None:
    accounts = _load()
    if username in accounts:
        raise ValueError('Account exists')
    salt = os.urandom(8).hex()
    passhash = _hash_password(password, salt)
    accounts[username] = {
        'salt': salt,
        'passhash': passhash,
        'administrator': bool(admin),
    }
    _save(accounts)


def authenticate(username: str, password: str) -> bool:
    accounts = _load()
    info = accounts.get(username)
    if not info:
        return False
    return _hash_password(password, info.get('salt', '')) == info.get('passhash')


def is_admin(username: str) -> bool:
    accounts = _load()
    return bool(accounts.get(username, {}).get('administrator'))

