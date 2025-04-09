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

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    # Check if Music Assistant is installed and available
    if "mass" not in hass.data:
        raise CannotConnect("Music Assistant is not installed or configured")
    
    # Return validated data
    return {"title": DEFAULT_NAME}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Music Assistant Spotify Lovelace."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                
                # Check if the integration is already configured
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host", default="your.public.ip.here"): str,
                vol.Required("port", default=8095): int,
                vol.Optional("ssl", default=False): bool,
            }),
            errors=errors,
        )



class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""