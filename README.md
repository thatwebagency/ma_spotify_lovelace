# Music Assistant Spotify Lovelace

A custom Home Assistant integration that allows controlling Music Assistant speakers and playing Spotify music directly from a custom Lovelace card.

## Features

- Control Music Assistant speakers (play, pause, stop, volume, next/previous track)
- Search Spotify for tracks, albums, artists, and playlists
- Play Spotify content on any Music Assistant speaker
- Custom Lovelace card for easy access from your dashboard

## Requirements

- Home Assistant
- [Music Assistant](https://github.com/music-assistant/hass-music-assistant) integration with Spotify provider configured
- HACS (for easy installation)

## Installation

### HACS Installation (Preferred)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add the URL of this repository and select "Integration" as the category
6. Click "Add"
7. Search for "Music Assistant Spotify Lovelace" and install it
8. Restart Home Assistant

### Manual Installation

1. Download the source code from this repository
2. Copy the `custom_components/ma_spotify_lovelace` directory to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Music Assistant Spotify Lovelace"
4. Click on it and follow the configuration steps

## Usage

### Adding the Card to Your Dashboard

1. Edit your dashboard
2. Click the "+" button to add a new card
3. Scroll down and select "Music Assistant Spotify Card" (under "Custom" section)
4. Click "Save"

### Using the Card

1. Select a speaker from the dropdown
2. Use the "Search" tab to find and play music:
   - Enter a search term
   - Select the content type (track, album, artist, playlist)
   - Click search
   - Click on a result to play it on the selected speaker
3. Use the "Controls" tab to control playback:
   - Play/Pause/Stop
   - Next/Previous track
   - Volume control

## Services

The integration provides the following services:

### play_spotify

Play Spotify content on a Music Assistant speaker.

| Parameter | Description | Required |
|-----------|-------------|----------|
| query | The search term or content ID | Yes |
| speaker_id | The ID of the speaker to play on | Yes |
| content_type | The type of content (track, album, artist, playlist) | No (default: track) |

### control_speaker

Control a Music Assistant speaker.

| Parameter | Description | Required |
|-----------|-------------|----------|
| speaker_id | The ID of the speaker to control | Yes |
| command | The command to execute (play, pause, stop, volume_set, volume_up, volume_down, next_track, previous_track) | Yes |
| value | Value for commands that require it (e.g., volume_set) | No |

## Troubleshooting

### Card Not Appearing in the Dashboard

If the card doesn't appear in your dashboard card picker:

1. Make sure you've restarted Home Assistant after installing the integration
2. Check the browser console for any JavaScript errors
3. Try clearing your browser cache

### Unable to Find Speakers

If no speakers are appearing in the dropdown:

1. Make sure Music Assistant is properly configured
2. Check that you have added at least one player in Music Assistant
3. Restart Home Assistant and refresh the page

### Search Not Working

If search isn't returning any results:

1. Ensure Spotify is properly configured in Music Assistant
2. Check that your Spotify account has the necessary permissions
3. Try a different search term

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.