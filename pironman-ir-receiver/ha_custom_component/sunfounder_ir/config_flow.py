"""Configure the independently running SunFounder IR bridge receiver ID."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "sunfounder_ir"


class SunFounderIRFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            receiver_id = user_input["receiver_id"].strip()
            if not receiver_id or len(receiver_id) > 64 or any(c.isspace() for c in receiver_id):
                return self.async_show_form(step_id="user", data_schema=self._schema(), errors={"base": "invalid_receiver_id"})
            await self.async_set_unique_id(receiver_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f"SunFounder IR ({receiver_id})", data={"receiver_id": receiver_id})
        return self.async_show_form(step_id="user", data_schema=self._schema())

    @staticmethod
    def _schema():
        return vol.Schema({vol.Required("receiver_id", default="pironman5-max"): str})
