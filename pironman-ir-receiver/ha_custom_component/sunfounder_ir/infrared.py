"""Native Home Assistant IR receiver for SunFounder standalone add-on events."""
from __future__ import annotations

from homeassistant.components.infrared import InfraredReceivedSignal, InfraredReceiverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

EVENT = "sunfounder_ir_received"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, add: AddEntitiesCallback) -> None:
    add([SunFounderReceiver(entry.data["receiver_id"])])


def valid_timings(values: object) -> bool:
    if not isinstance(values, list) or not 8 <= len(values) <= 512:
        return False
    for index, value in enumerate(values):
        if type(value) is not int or value == 0 or abs(value) > 1_000_000:
            return False
        if (value > 0) != (index % 2 == 0):
            return False
    return True


class SunFounderReceiver(InfraredReceiverEntity):
    _attr_has_entity_name = True
    _attr_name = "IR Receiver"

    def __init__(self, receiver_id: str) -> None:
        self.receiver_id = receiver_id
        self._attr_unique_id = f"sunfounder_ir_{receiver_id}"
        self._attr_device_info = {
            "identifiers": {("sunfounder_ir", receiver_id)},
            "name": f"SunFounder IR ({receiver_id})",
            "manufacturer": "SunFounder",
            "model": "Pironman 5 Max IR Receiver",
        }
        self._unsub = None

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._unsub = self.hass.bus.async_listen(EVENT, self._handle_event)

    @callback
    def _handle_event(self, event: Event) -> None:
        data = event.data
        if data.get("receiver_id") != self.receiver_id:
            return
        timings = data.get("timings")
        if not valid_timings(timings):
            return
        self._handle_received_signal(InfraredReceivedSignal(timings=timings, modulation=None))

    async def async_will_remove_from_hass(self) -> None:
        if self._unsub:
            self._unsub()
            self._unsub = None
        await super().async_will_remove_from_hass()
