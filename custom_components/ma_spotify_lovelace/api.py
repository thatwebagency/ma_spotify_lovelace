"""API client for Music Assistant."""
from __future__ import annotations

import logging
from typing import Any, Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.components import music_assistant as mass

_LOGGER = logging.getLogger(__name__)

class MusicAssistantApi:
    """API client for Music Assistant."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the API client."""
        self.hass = hass
        self.mass = None

    async def async_setup(self) -> None:
        """Set up the API client."""
        try:
            # Get the Music Assistant instance
            self.mass = self.hass.data.get("mass")
            if not self.mass:
                _LOGGER.error("Music Assistant not found. Please install and configure it first.")
                return False
            _LOGGER.info("Successfully connected to Music Assistant")
            return True
        except Exception as err:
            _LOGGER.error("Error setting up Music Assistant API: %s", err)
            return False

    async def async_teardown(self) -> None:
        """Tear down the API client."""
        self.mass = None

    async def get_speakers(self) -> list[dict[str, Any]]:
        """Get all available Music Assistant speakers."""
        if not self.mass:
            _LOGGER.error("Music Assistant not available")
            return []
        
        try:
            players = await self.mass.mass_api.players()
            return [
                {
                    "id": player.player_id,
                    "name": player.display_name,
                    "available": player.available,
                    "powered": player.powered,
                    "volume_level": player.volume_level,
                    "is_playing": player.state == "playing"
                }
                for player in players.values()
            ]
        except Exception as err:
            _LOGGER.error("Failed to get speakers: %s", err)
            return []

    async def control_speaker(self, speaker_id: str, command: str, value: Optional[Any] = None) -> bool:
        """Control a Music Assistant speaker."""
        if not self.mass:
            _LOGGER.error("Music Assistant not available")
            return False
        
        try:
            # Get the player from MA
            player = await self.mass.mass_api.get_player(speaker_id)
            if not player:
                _LOGGER.error("Speaker %s not found", speaker_id)
                return False
            
            # Execute the command
            if command == "play":
                await self.mass.mass_api.player_play(speaker_id)
            elif command == "pause":
                await self.mass.mass_api.player_pause(speaker_id)
            elif command == "stop":
                await self.mass.mass_api.player_stop(speaker_id)
            elif command == "volume_set" and value is not None:
                await self.mass.mass_api.player_volume_set(speaker_id, float(value))
            elif command == "volume_up":
                current_vol = player.volume_level
                await self.mass.mass_api.player_volume_set(speaker_id, min(current_vol + 0.1, 1.0))
            elif command == "volume_down":
                current_vol = player.volume_level
                await self.mass.mass_api.player_volume_set(speaker_id, max(current_vol - 0.1, 0.0))
            elif command == "next_track":
                await self.mass.mass_api.player_next(speaker_id)
            elif command == "previous_track":
                await self.mass.mass_api.player_previous(speaker_id)
            else:
                _LOGGER.error("Unknown command: %s", command)
                return False
            
            return True
        except Exception as err:
            _LOGGER.error("Failed to control speaker %s with command %s: %s", speaker_id, command, err)
            return False

    async def search_and_play(self, query: str, speaker_id: str, content_type: str = "track") -> bool:
        """Search Spotify for content and play it on the selected speaker."""
        if not self.mass:
            _LOGGER.error("Music Assistant not available")
            return False
        
        try:
            # Search for content
            search_results = await self.mass.mass_api.search(
                query, media_types=[content_type], limit=10, providers=["spotify"]
            )
            
            if not search_results or not search_results.get(content_type):
                _LOGGER.error("No %s found for query: %s", content_type, query)
                return False
            
            # Get the first result
            item = search_results[content_type][0]
            item_id = item.item_id
            
            # Play the content
            if content_type == "track":
                await self.mass.mass_api.play_media(speaker_id, item_id)
            elif content_type == "album":
                await self.mass.mass_api.play_media(speaker_id, item_id, "album")
            elif content_type == "artist":
                await self.mass.mass_api.play_media(speaker_id, item_id, "artist")
            elif content_type == "playlist":
                await self.mass.mass_api.play_media(speaker_id, item_id, "playlist")
            else:
                _LOGGER.error("Unsupported content type: %s", content_type)
                return False
            
            return True
        except Exception as err:
            _LOGGER.error("Failed to search and play: %s", err)
            return False