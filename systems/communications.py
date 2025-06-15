"""Communication systems for MUDpy SS13.

This module implements a very lightweight simulation of the station
communication network.  It provides radio channels, intercom links,
personal data assistants (PDAs) and a simple announcement queue.

The goal of this module is not to be a full reproduction of Space
Station 13 communications, but rather to expose hooks that other parts
of the engine can build upon.  Messages are dispatched through the
``events`` publish/subscribe system so that game logic or the server
layer can react accordingly.
"""

from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class RadioChannel:
    """Definition for a radio frequency."""

    name: str
    department: str
    encrypted: bool = False
    key: Optional[str] = None


@dataclass
class PDADevice:
    """Simple representation of a PDA."""

    device_id: str
    owner_id: str
    apps: List[str] = field(default_factory=list)


class CommunicationsSystem:
    """Central manager for in game communications."""

    def __init__(self) -> None:
        self.channels: Dict[str, RadioChannel] = {}
        self.intercom_links: Dict[str, List[str]] = {}
        self.pdas: Dict[str, PDADevice] = {}
        self.jammed_channels: set[str] = set()
        self.dead_zones: set[str] = set()
        self.announcement_queue: List[Tuple[int, str]] = []
        self.radio_logs: Dict[str, List[Tuple[str, str]]] = {}
        self.pda_logs: Dict[str, List[Tuple[str, str]]] = {}
        self.pda_keys: Dict[str, str] = {}
        self.max_log = 50

    # ------------------------------------------------------------------
    def register_channel(
        self,
        name: str,
        department: str,
        encrypted: bool = False,
        key: Optional[str] = None,
    ) -> None:
        """Register a radio channel."""

        if encrypted and not key:
            key = secrets.token_hex(4)
        self.channels[name] = RadioChannel(name, department, encrypted, key)
        logger.debug("Registered radio channel %s", name)

    # ------------------------------------------------------------------
    def jam_channel(self, name: str) -> None:
        """Temporarily jam a radio channel."""

        self.jammed_channels.add(name)
        publish("channel_jammed", channel=name)

    # ------------------------------------------------------------------
    def unjam_channel(self, name: str) -> None:
        if name in self.jammed_channels:
            self.jammed_channels.remove(name)
            publish("channel_unjammed", channel=name)

    # ------------------------------------------------------------------
    def send_radio(
        self,
        sender_id: str,
        channel: str,
        message: str,
        *,
        location: Optional[str] = None,
        key: Optional[str] = None,
    ) -> bool:
        """Send a message over a radio channel."""

        ch = self.channels.get(channel)
        if not ch:
            return False
        if channel in self.jammed_channels:
            return False
        if location and location in self.dead_zones:
            return False

        text = message
        if ch.encrypted:
            if key != ch.key:
                return False
            text = self._encrypt(message, ch.key)

        log = self.radio_logs.setdefault(channel, [])
        log.append((sender_id, message))
        if len(log) > self.max_log:
            log.pop(0)

        publish("radio_message", channel=channel, sender=sender_id, message=text)
        return True

    # ------------------------------------------------------------------
    def _encrypt(self, text: str, key: str) -> str:
        """Very small XOR cipher for demonstration."""

        return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

    # ------------------------------------------------------------------
    def _decrypt(self, text: str, key: str) -> str:
        return self._encrypt(text, key)

    # ------------------------------------------------------------------
    def register_intercom(
        self, room_id: str, connections: Optional[List[str]] = None
    ) -> None:
        """Create an intercom node that can talk to other rooms."""

        self.intercom_links[room_id] = connections or []

    # ------------------------------------------------------------------
    def send_intercom(
        self, room_id: str, message: str, priority: str = "normal"
    ) -> bool:
        if room_id in self.dead_zones:
            return False
        targets = self.intercom_links.get(room_id, [])
        publish(
            "intercom_message",
            room=room_id,
            targets=targets,
            message=message,
            priority=priority,
        )
        return True

    # ------------------------------------------------------------------
    def register_pda(self, device_id: str, owner_id: str) -> None:
        self.pdas[device_id] = PDADevice(device_id, owner_id)

    def get_radio_log(self, channel: str) -> List[Tuple[str, str]]:
        return list(self.radio_logs.get(channel, []))

    def get_pda_log(self, device_id: str) -> List[Tuple[str, str]]:
        return list(self.pda_logs.get(device_id, []))

    # ------------------------------------------------------------------
    def generate_pda_key(self, device_id: str) -> Optional[str]:
        if device_id not in self.pdas:
            return None
        key = secrets.token_hex(4)
        self.pda_keys[device_id] = key
        return key

    # ------------------------------------------------------------------
    def clear_radio_log(self, channel: str) -> None:
        self.radio_logs.pop(channel, None)

    # ------------------------------------------------------------------
    def clear_pda_log(self, device_id: str) -> None:
        self.pda_logs.pop(device_id, None)

    # ------------------------------------------------------------------
    def send_pda_message(
        self,
        sender_device: str,
        target_device: str,
        text: str,
        *,
        file: Optional[str] = None,
        key: Optional[str] = None,
    ) -> bool:
        if sender_device not in self.pdas or target_device not in self.pdas:
            return False
        target_key = self.pda_keys.get(target_device)
        send_text = text
        if target_key:
            if key != target_key:
                return False
            send_text = self._encrypt(text, target_key)

        log = self.pda_logs.setdefault(target_device, [])
        log.append((sender_device, text))
        if len(log) > self.max_log:
            log.pop(0)

        publish(
            "pda_message",
            sender=sender_device,
            target=target_device,
            text=send_text,
            file=file,
        )
        return True

    # ------------------------------------------------------------------
    def announce(
        self, message: str, priority: int = 1, emergency: bool = False
    ) -> None:
        """Broadcast a station wide announcement."""

        self.announcement_queue.append((priority, message))
        self.announcement_queue.sort(key=lambda p: p[0], reverse=True)
        publish(
            "station_announcement",
            message=message,
            priority=priority,
            emergency=emergency,
        )

    # ------------------------------------------------------------------
    def set_dead_zone(self, room_id: str, dead: bool = True) -> None:
        if dead:
            self.dead_zones.add(room_id)
        else:
            self.dead_zones.discard(room_id)


# Global instance ------------------------------------------------------
COMMUNICATIONS_SYSTEM = CommunicationsSystem()


def get_comms_system() -> CommunicationsSystem:
    """Return the global communications system."""

    return COMMUNICATIONS_SYSTEM
