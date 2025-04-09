"""The Music Assistant Spotify Lovelace integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.components import frontend

from .const import DOMAIN, CONF_MA_INSTANCE, SERVICE_PLAY_SPOTIFY, SERVICE_CONTROL_SPEAKER
from .api import MusicAssistantApi

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Optional(CONF_MA_INSTANCE): cv.string,
        })
    },
    extra=vol.ALLOW_EXTRA,
)

# Define the services schema
SERVICE_PLAY_SPOTIFY_SCHEMA = vol.Schema({
    vol.Required("query"): cv.string,
    vol.Required("speaker_id"): cv.string,
    vol.Optional("content_type"): cv.string,
})

SERVICE_CONTROL_SPEAKER_SCHEMA = vol.Schema({
    vol.Required("speaker_id"): cv.string,
    vol.Required("command"): cv.string,
    vol.Optional("value"): vol.Any(cv.string, cv.positive_float),  
})

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Music Assistant Spotify Lovelace component."""
    hass.data.setdefault(DOMAIN, {})
    
    # Register services
    async def play_spotify(call: ServiceCall) -> None:
        """Handle the service call to play Spotify content."""
        query = call.data.get("query")
        speaker_id = call.data.get("speaker_id")
        content_type = call.data.get("content_type", "track")
        
        api: MusicAssistantApi = hass.data[DOMAIN]["api"]
        await api.search_and_play(query, speaker_id, content_type)

    async def control_speaker(call: ServiceCall) -> None:
        """Handle the service call to control a speaker."""
        speaker_id = call.data.get("speaker_id")
        command = call.data.get("command")
        value = call.data.get("value", None)
        
        api: MusicAssistantApi = hass.data[DOMAIN]["api"]
        await api.control_speaker(speaker_id, command, value)

    hass.services.async_register(
        DOMAIN, SERVICE_PLAY_SPOTIFY, play_spotify, schema=SERVICE_PLAY_SPOTIFY_SCHEMA
    )
    
    hass.services.async_register(
        DOMAIN, SERVICE_CONTROL_SPEAKER, control_speaker, schema=SERVICE_CONTROL_SPEAKER_SCHEMA
    )
    
    # Register card resources
    frontend.async_register_built_in_panel(
        hass,
        component_name="lovelace",
        sidebar_title="Music Assistant Spotify",
        sidebar_icon="mdi:spotify",
        frontend_url_path="ma-spotify",
        require_admin=False,
        config={"mode": "storage"},
    )
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Music Assistant Spotify Lovelace from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Initialize API connection to Music Assistant
    api = MusicAssistantApi(hass)
    await api.async_setup()
    
    hass.data[DOMAIN]["api"] = api
    hass.data[DOMAIN]["config_entry"] = entry
    
    # Load the custom card
    hass.http.register_static_path(
        f"/static/community/{DOMAIN}",
        hass.config.path(f"custom_components/{DOMAIN}/lovelace"),
    )
    
    frontend.async_register_extra_js_module(
        hass, f"/static/community/{DOMAIN}/ma-spotify-card.js"
    )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if "api" in hass.data[DOMAIN]:
        await hass.data[DOMAIN]["api"].async_teardown()
    
    hass.data.pop(DOMAIN)
    return True