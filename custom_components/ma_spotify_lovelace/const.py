"""Constants for the Music Assistant Spotify Lovelace integration."""

DOMAIN = "ma_spotify_lovelace"

# Configuration constants
CONF_MA_INSTANCE = "music_assistant_instance"

# Service names
SERVICE_PLAY_SPOTIFY = "play_spotify"
SERVICE_CONTROL_SPEAKER = "control_speaker"

# Speaker commands
CMD_PLAY = "play"
CMD_PAUSE = "pause"
CMD_STOP = "stop"
CMD_VOLUME_SET = "volume_set"
CMD_VOLUME_UP = "volume_up"
CMD_VOLUME_DOWN = "volume_down"
CMD_NEXT_TRACK = "next_track"
CMD_PREVIOUS_TRACK = "previous_track"

# Content types
CONTENT_TYPE_TRACK = "track"
CONTENT_TYPE_ALBUM = "album"
CONTENT_TYPE_ARTIST = "artist"
CONTENT_TYPE_PLAYLIST = "playlist"

# Default values
DEFAULT_NAME = "Music Assistant Spotify"