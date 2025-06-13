import asyncio
from unittest import mock

import sys
import os
import yaml

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import random_events
from systems.random_events import RandomEventSystem


def test_load_random_events():
    # reload events from yaml
    random_events.load_random_events("data/random_events.yaml")
    with open("data/random_events.yaml", "r") as f:
        data = yaml.safe_load(f) or []
    expected_ids = [evt["id"] for evt in data]
    assert list(random_events.RANDOM_EVENTS.keys()) == expected_ids


def test_random_event_system_update_publishes_event(monkeypatch):
    system = RandomEventSystem("data/random_events.yaml")
    system.load_events()
    # compute weights attribute expected by update()
    system.weights = [evt.weight for evt in system.events]

    mock_publish = mock.Mock()
    monkeypatch.setattr("events.publish", mock_publish)
    monkeypatch.setattr(random_events, "publish", mock_publish)
    import systems.random_events as sr
    monkeypatch.setattr(sr, "publish", mock_publish)
    monkeypatch.setattr("random.choices", lambda seq, weights=None, k=1: [seq[0]])

    asyncio.run(system.update())

    # First call publishes the event id
    assert mock_publish.call_count == 2
    event_id = system.events[0].id
    first_call = mock_publish.call_args_list[0]
    assert first_call.args[0] == event_id
    second_call = mock_publish.call_args_list[1]
    assert second_call.args[0] == "random_event"
    assert second_call.kwargs.get("event_id") == event_id


def test_trigger_event_returns_bool(monkeypatch):
    random_events.load_random_events("data/random_events.yaml")
    mock_publish = mock.Mock()
    monkeypatch.setattr("events.publish", mock_publish)
    monkeypatch.setattr(random_events, "publish", mock_publish)

    assert random_events.trigger_event("meteor_shower") is True
    assert random_events.trigger_event("does_not_exist") is False
    # two events should have been published for the valid call
    assert mock_publish.call_count == 2
