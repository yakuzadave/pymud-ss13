"""Restricted scripting engine for in-game verbs."""

from __future__ import annotations

import logging
import os
from typing import Any, Callable, Dict, List, Optional

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

logger = logging.getLogger(__name__)


class ScriptEngine:
    """Manage restricted scripts and verb execution."""

    def __init__(self) -> None:
        self.scripts: Dict[str, Dict[str, Any]] = {}
        self.api: Dict[str, Callable] = {}

    # --------------------------------------------------------------
    def register_api(self, name: str, func: Callable) -> None:
        """Expose a function to scripts."""
        self.api[name] = func

    # --------------------------------------------------------------
    def register_script(
        self,
        script_id: str,
        code: str,
        owner_id: str,
        *,
        obj_id: Optional[str] = None,
        verb: Optional[str] = None,
    ) -> bool:
        """Compile and register a script."""
        try:
            byte_code = compile_restricted(code, script_id, "exec")
        except Exception as exc:  # pragma: no cover - compile errors
            logger.error("Failed compiling %s: %s", script_id, exc)
            return False
        self.scripts[script_id] = {
            "code": code,
            "byte_code": byte_code,
            "owner_id": owner_id,
            "obj_id": obj_id,
            "verb": verb,
        }
        return True

    # --------------------------------------------------------------
    def remove_script(self, script_id: str) -> bool:
        if script_id in self.scripts:
            del self.scripts[script_id]
            return True
        return False

    # --------------------------------------------------------------
    def get_script_info(self, script_id: str) -> Optional[Dict[str, Any]]:
        return self.scripts.get(script_id)

    # --------------------------------------------------------------
    def list_scripts(self, owner_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        if owner_id:
            return {sid: info for sid, info in self.scripts.items() if info.get("owner_id") == owner_id}
        return self.scripts.copy()

    # --------------------------------------------------------------
    def execute_script(self, script_id: str, context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        script = self.scripts.get(script_id)
        if not script:
            logger.warning("Unknown script %s", script_id)
            return None

        glb = {"__builtins__": safe_builtins}
        glb.update(self.api)
        loc = context.copy() if context else {}
        try:
            exec(script["byte_code"], glb, loc)
            return loc
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.error("Error executing %s: %s", script_id, exc)
            return None

    # --------------------------------------------------------------
    def add_verb(self, obj_id: str, verb: str, code: str, owner_id: str) -> Optional[str]:
        script_id = f"{obj_id}:{verb}"
        if self.register_script(script_id, code, owner_id, obj_id=obj_id, verb=verb):
            return script_id
        return None

    # --------------------------------------------------------------
    def run_verb(self, obj_id: str, verb: str, context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        script_id = f"{obj_id}:{verb}"
        return self.execute_script(script_id, context)

    # --------------------------------------------------------------
    def to_list(self) -> List[Dict[str, Any]]:
        data: List[Dict[str, Any]] = []
        for sid, info in self.scripts.items():
            data.append(
                {
                    "id": sid,
                    "code": info["code"],
                    "owner_id": info["owner_id"],
                    "obj_id": info.get("obj_id"),
                    "verb": info.get("verb"),
                }
            )
        return data

    # --------------------------------------------------------------
    def load_list(self, data: List[Dict[str, Any]]) -> None:
        for entry in data:
            self.register_script(
                entry["id"],
                entry.get("code", ""),
                entry.get("owner_id", ""),
                obj_id=entry.get("obj_id"),
                verb=entry.get("verb"),
            )

    # --------------------------------------------------------------
    def save_to_file(self, path: str) -> None:
        import yaml

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            yaml.safe_dump(self.to_list(), fh, default_flow_style=False)

    # --------------------------------------------------------------
    def load_from_file(self, path: str) -> None:
        import yaml

        if not os.path.exists(path):
            return
        with open(path, "r") as fh:
            data = yaml.safe_load(fh) or []
        if isinstance(data, list):
            self.load_list(data)


SCRIPT_ENGINE = ScriptEngine()


def get_script_engine() -> ScriptEngine:
    return SCRIPT_ENGINE
