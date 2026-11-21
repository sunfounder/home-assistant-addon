"""Standalone contract tests for the SunFounder IR Home Assistant adapter.

Home Assistant dependencies are stubbed intentionally so these tests run in
standard-library-only CI. Full HAOS integration is verified separately by users.
"""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock


def load_infrared_module():
    # Provide the minimal Home Assistant interfaces imported by infrared.py.
    ha = types.ModuleType("homeassistant")
    ha.__path__ = []
    components = types.ModuleType("homeassistant.components")
    components.__path__ = []
    infrared = types.ModuleType("homeassistant.components.infrared")

    class InfraredReceiverEntity:
        async def async_added_to_hass(self):
            pass

        async def async_will_remove_from_hass(self):
            pass

        def _handle_received_signal(self, signal):
            self.received.append(signal)

    class InfraredReceivedSignal:
        def __init__(self, *, timings, modulation):
            self.timings = timings
            self.modulation = modulation

    infrared.InfraredReceiverEntity = InfraredReceiverEntity
    infrared.InfraredReceivedSignal = InfraredReceivedSignal
    config_entries = types.ModuleType("homeassistant.config_entries")
    config_entries.ConfigEntry = type("ConfigEntry", (), {})
    core = types.ModuleType("homeassistant.core")
    core.Event = type("Event", (), {})
    core.HomeAssistant = type("HomeAssistant", (), {})
    core.callback = lambda fn: fn
    helpers = types.ModuleType("homeassistant.helpers")
    helpers.__path__ = []
    entity_platform = types.ModuleType("homeassistant.helpers.entity_platform")
    entity_platform.AddEntitiesCallback = type("AddEntitiesCallback", (), {})

    mocks = {
        "homeassistant": ha,
        "homeassistant.components": components,
        "homeassistant.components.infrared": infrared,
        "homeassistant.config_entries": config_entries,
        "homeassistant.core": core,
        "homeassistant.helpers": helpers,
        "homeassistant.helpers.entity_platform": entity_platform,
    }
    previous = {name: sys.modules.get(name) for name in mocks}
    try:
        sys.modules.update(mocks)
        path = Path(__file__).parents[1] / "ha_custom_component" / "sunfounder_ir" / "infrared.py"
        spec = importlib.util.spec_from_file_location("sunfounder_ir_adapter_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for name, original in previous.items():
            if original is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = original


adapter = load_infrared_module()
GOOD = [560, -560] * 5


class TestTimingValidation(unittest.TestCase):
    def test_valid_frame(self):
        self.assertTrue(adapter.valid_timings(GOOD))

    def test_invalid_frames(self):
        cases = [None, {}, "560,-560", [], GOOD[:7], GOOD * 52,
                 [True, -560] * 5, [0, -560] * 5,
                 [560, 560] * 5, [-560, 560] * 5,
                 [1_000_001, -560] * 5, [560.0, -560] * 5]
        for timings in cases:
            with self.subTest(timings=str(timings)[:50]):
                self.assertFalse(adapter.valid_timings(timings))


class TestReceiverEvents(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.handlers = {}
        self.unsub = Mock()
        bus = Mock()

        def register(event, callback):
            self.handlers[event] = callback
            return self.unsub

        bus.async_listen.side_effect = register
        self.receiver = adapter.SunFounderReceiver("pironman5-max")
        self.receiver.hass = types.SimpleNamespace(bus=bus)
        self.receiver.received = []
        await self.receiver.async_added_to_hass()

    async def asyncTearDown(self):
        await self.receiver.async_will_remove_from_hass()

    def fire(self, receiver_id="pironman5-max", timings=None):
        event = types.SimpleNamespace(data={"receiver_id": receiver_id,
                                            "timings": GOOD if timings is None else timings})
        self.handlers[adapter.EVENT](event)

    async def test_matching_receiver_delivers_signal(self):
        self.fire()
        self.assertEqual(len(self.receiver.received), 1)
        self.assertEqual(self.receiver.received[0].timings, GOOD)
        self.assertIsNone(self.receiver.received[0].modulation)

    async def test_other_receiver_is_ignored(self):
        self.fire(receiver_id="another-pironman")
        self.assertEqual(self.receiver.received, [])

    async def test_invalid_frame_is_ignored(self):
        self.fire(timings=[560, -560])
        self.assertEqual(self.receiver.received, [])

    async def test_listener_is_removed(self):
        await self.receiver.async_will_remove_from_hass()
        self.unsub.assert_called_once()
        self.receiver._unsub = None  # teardown should be idempotent


if __name__ == "__main__":
    unittest.main()
