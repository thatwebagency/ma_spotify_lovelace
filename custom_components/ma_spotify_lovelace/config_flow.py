"""Config flow for Music Assistant Spotify Lovelace integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_MA_INSTANCE, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

async def validate_input(hass: HomeAssistant):
    if "mass" not in hass.data:
        raise CannotConnect  # or make a new custom exception like MusicAssistantNotAvailable
    return {"title": DEFAULT_NAME}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Music Assistant Spotify Lovelace."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        errors = {}

        if user_input is not None:
            try:
                await validate_input(self.hass)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title="Music Assistant Spotify", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),  # no fields needed
            errors=errors,
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""