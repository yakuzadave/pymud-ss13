"""Simple mod management for MUDpy SS13.

This module provides utilities for discovering and loading optional
content packs ("mods"). Mods can supply YAML content files and Python
scripts that extend the base game. Each mod lives in its own directory
within the ``mods/`` folder and must include a ``mod.yaml`` metadata
file.
"""

from __future__ import annotations

import importlib.util
import logging
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import yaml

from world import WORLD

logger = logging.getLogger(__name__)


@dataclass
class Mod:
    """Metadata and resources for a single mod."""

    name: str
    path: str
    version: str = "0.0.1"
    description: str = ""
    dependencies: List[str] = field(default_factory=list)


class ModManager:
    """Discover and load mods from a directory."""

    def __init__(self, mods_dir: str = "mods", world: Optional[object] = None) -> None:
        self.mods_dir = mods_dir
        self.world = world or WORLD
        self.mods: Dict[str, Mod] = {}

    def discover(self) -> List[str]:
        """Search ``mods_dir`` for available mods."""
        if not os.path.isdir(self.mods_dir):
            logger.info("No mods directory found")
            return []

        discovered: List[str] = []
        for entry in os.listdir(self.mods_dir):
            mod_path = os.path.join(self.mods_dir, entry)
            meta_path = os.path.join(mod_path, "mod.yaml")
            if os.path.isdir(mod_path) and os.path.isfile(meta_path):
                with open(meta_path, "r") as f:
                    meta = yaml.safe_load(f) or {}
                mod = Mod(
                    name=meta.get("name", entry),
                    path=mod_path,
                    version=str(meta.get("version", "0.0.1")),
                    description=meta.get("description", ""),
                    dependencies=meta.get("dependencies", []),
                )
                self.mods[mod.name] = mod
                discovered.append(mod.name)
                logger.info(f"Discovered mod {mod.name} v{mod.version}")
        return discovered

    def load_mod(self, name: str) -> bool:
        """Load a single mod by name."""
        mod = self.mods.get(name)
        if not mod:
            logger.warning(f"Unknown mod {name}")
            return False

        self._load_content(mod)
        self._load_scripts(mod)
        logger.info(f"Loaded mod {mod.name} v{mod.version}")
        return True

    def load_all(self) -> List[str]:
        """Load all discovered mods."""
        loaded: List[str] = []
        for name in list(self.mods):
            if self.load_mod(name):
                loaded.append(name)
        return loaded

    # Internal helpers -------------------------------------------------
    def _load_content(self, mod: Mod) -> None:
        content_dir = os.path.join(mod.path, "content")
        if not os.path.isdir(content_dir):
            return
        for fname in os.listdir(content_dir):
            if fname.endswith(".yaml"):
                path = os.path.join(content_dir, fname)
                try:
                    self.world.load_from_file(path)
                    logger.debug(f"Loaded content from {path}")
                except Exception as exc:
                    logger.error(f"Failed loading {path}: {exc}")

    def _load_scripts(self, mod: Mod) -> None:
        scripts_dir = os.path.join(mod.path, "scripts")
        if not os.path.isdir(scripts_dir):
            return
        for fname in os.listdir(scripts_dir):
            if fname.endswith(".py"):
                path = os.path.join(scripts_dir, fname)
                module_name = f"{mod.name}.{os.path.splitext(fname)[0]}"
                try:
                    spec = importlib.util.spec_from_file_location(module_name, path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        logger.debug(f"Executed script {path}")
                except Exception as exc:
                    logger.error(f"Failed executing script {path}: {exc}")
