const LitElement = Object.getPrototypeOf(
    customElements.get("ha-panel-lovelace")
  );
  const html = LitElement.prototype.html;
  const css = LitElement.prototype.css;
  
  class MusicAssistantSpotifyCard extends LitElement {
    static get properties() {
      return {
        hass: { type: Object },
        config: { type: Object },
        speakers: { type: Array },
        selectedSpeaker: { type: String },
        searchQuery: { type: String },
        searchResults: { type: Array },
        activeTab: { type: String },
        isLoading: { type: Boolean },
        currentTrack: { type: Object },
      };
    }
  
    constructor() {
      super();
      this.speakers = [];
      this.selectedSpeaker = "";
      this.searchQuery = "";
      this.searchResults = [];
      this.activeTab = "search";
      this.isLoading = false;
      this.contentType = "track";
      this.currentTrack = null;
    }
  
    setConfig(config) {
      if (!config) {
        throw new Error("Invalid configuration");
      }
      this.config = config;
    }
  
    async firstUpdated() {
      this.loadSpeakers();
    }
  
    async loadSpeakers() {
      this.isLoading = true;
      try {
        const resp = await this.hass.callWS({
          type: "ma_spotify_lovelace/get_speakers",
        });
        this.speakers = resp.speakers;
        if (this.speakers.length > 0 && !this.selectedSpeaker) {
          this.selectedSpeaker = this.speakers[0].id;
        }
      } catch (error) {
        console.error("Error loading speakers:", error);
      } finally {
        this.isLoading = false;
      }
    }
  
    async searchSpotify() {
      if (!this.searchQuery) return;
      
      this.isLoading = true;
      try {
        const resp = await this.hass.callWS({
          type: "ma_spotify_lovelace/search_spotify",
          query: this.searchQuery,
          content_type: this.contentType,
        });
        this.searchResults = resp.results;
      } catch (error) {
        console.error("Error searching Spotify:", error);
      } finally {
        this.isLoading = false;
      }
    }
  
    async playContent(itemId) {
      if (!this.selectedSpeaker) {
        alert("Please select a speaker first");
        return;
      }
      
      this.isLoading = true;
      try {
        await this.hass.callService("ma_spotify_lovelace", "play_spotify", {
          query: itemId,
          speaker_id: this.selectedSpeaker,
          content_type: this.contentType,
        });
      } catch (error) {
        console.error("Error playing content:", error);
      } finally {
        this.isLoading = false;
      }
    }
  
    async controlSpeaker(command, value = null) {
      if (!this.selectedSpeaker) {
        alert("Please select a speaker first");
        return;
      }
      
      try {
        const serviceData = {
          speaker_id: this.selectedSpeaker,
          command: command,
        };
        
        if (value !== null) {
          serviceData.value = value;
        }
        
        await this.hass.callService("ma_spotify_lovelace", "control_speaker", serviceData);
      } catch (error) {
        console.error(`Error executing command ${command}:`, error);
      }
    }
  
    handleSearchInput(e) {
      this.searchQuery = e.target.value;
    }
  
    handleSpeakerChange(e) {
      this.selectedSpeaker = e.target.value;
    }
  
    handleContentTypeChange(e) {
      this.contentType = e.target.value;
    }
  
    handleTabChange(tab) {
      this.activeTab = tab;
    }
  
    render() {
      return html`
        <ha-card header="Music Assistant Spotify">
          <div class="card-content">
            <div class="speaker-selector">
              <label for="speaker-select">Speaker:</label>
              <select id="speaker-select" @change="${this.handleSpeakerChange}">
                ${this.speakers.map(
                  (speaker) => html`
                    <option value="${speaker.id}" ?selected=${speaker.id === this.selectedSpeaker}>
                      ${speaker.name}
                    </option>
                  `
                )}
              </select>
              <button @click="${this.loadSpeakers}" class="refresh-btn">
                <ha-icon icon="mdi:refresh"></ha-icon>
              </button>
            </div>
            
            <div class="tabs">
              <button 
                class="${this.activeTab === 'search' ? 'active' : ''}" 
                @click="${() => this.handleTabChange('search')}">
                Search
              </button>
              <button 
                class="${this.activeTab === 'controls' ? 'active' : ''}" 
                @click="${() => this.handleTabChange('controls')}">
                Controls
              </button>
            </div>
            
            ${this.activeTab === 'search' ? this.renderSearchTab() : this.renderControlsTab()}
          </div>
        </ha-card>
      `;
    }
  
    renderSearchTab() {
      return html`
        <div class="search-container">
          <div class="search-header">
            <input 
              type="text" 
              placeholder="Search Spotify..." 
              @input="${this.handleSearchInput}" 
              value="${this.searchQuery}"
            />
            <select @change="${this.handleContentTypeChange}">
              <option value="track" ?selected=${this.contentType === "track"}>Tracks</option>
              <option value="album" ?selected=${this.contentType === "album"}>Albums</option>
              <option value="artist" ?selected=${this.contentType === "artist"}>Artists</option>
              <option value="playlist" ?selected=${this.contentType === "playlist"}>Playlists</option>
            </select>
            <button @click="${this.searchSpotify}" ?disabled=${!this.searchQuery}>
              <ha-icon icon="mdi:magnify"></ha-icon>
            </button>
          </div>
          
          ${this.isLoading ? html`<div class="loading">Loading...</div>` : ''}
          
          <div class="search-results">
            ${this.searchResults.map(
              (item) => html`
                <div class="result-item" @click="${() => this.playContent(item.id)}">
                  ${item.image ? html`<img src="${item.image}" alt="${item.name}" />` : ''}
                  <div class="item-info">
                    <div class="item-name">${item.name}</div>
                    ${item.artist ? html`<div class="item-artist">${item.artist}</div>` : ''}
                  </div>
                  <ha-icon icon="mdi:play-circle"></ha-icon>
                </div>
              `
            )}
          </div>
        </div>
      `;
    }
  
    renderControlsTab() {
      return html`
        <div class="controls-container">
          <div class="playback-controls">
            <button @click="${() => this.controlSpeaker('previous_track')}">
              <ha-icon icon="mdi:skip-previous"></ha-icon>
            </button>
            <button @click="${() => this.controlSpeaker('play')}">
              <ha-icon icon="mdi:play"></ha-icon>
            </button>
            <button @click="${() => this.controlSpeaker('pause')}">
              <ha-icon icon="mdi:pause"></ha-icon>
            </button>
            <button @click="${() => this.controlSpeaker('stop')}">
              <ha-icon icon="mdi:stop"></ha-icon>
            </button>
            <button @click="${() => this.controlSpeaker('next_track')}">
              <ha-icon icon="mdi:skip-next"></ha-icon>
            </button>
          </div>
          
          <div class="volume-controls">
            <button @click="${() => this.controlSpeaker('volume_down')}">
              <ha-icon icon="mdi:volume-minus"></ha-icon>
            </button>
            <input 
              type="range" 
              min="0" 
              max="100" 
              @change="${(e) => this.controlSpeaker('volume_set', e.target.value / 100)}"
            />
            <button @click="${() => this.controlSpeaker('volume_up')}">
              <ha-icon icon="mdi:volume-plus"></ha-icon>
            </button>
          </div>
        </div>
      `;
    }
  
    static get styles() {
      return css`
        ha-card {
          padding-bottom: 16px;
        }
        
        .card-content {
          padding: 16px;
        }
        
        .speaker-selector {
          display: flex;
          align-items: center;
          margin-bottom: 16px;
        }
        
        .speaker-selector label {
          margin-right: 8px;
        }
        
        .speaker-selector select {
          flex-grow: 1;
          padding: 8px;
          border-radius: 4px;
        }
        
        .refresh-btn {
          background: none;
          border: none;
          cursor: pointer;
          color: var(--primary-color);
        }
        
        .tabs {
          display: flex;
          margin-bottom: 16px;
          border-bottom: 1px solid var(--divider-color);
        }
        
        .tabs button {
          background: none;
          border: none;
          padding: 8px 16px;
          cursor: pointer;
          flex-grow: 1;
        }
        
        .tabs button.active {
          font-weight: bold;
          border-bottom: 2px solid var(--primary-color);
        }
        
        .search-header {
          display: flex;
          margin-bottom: 16px;
        }
        
        .search-header input {
          flex-grow: 1;
          padding: 8px;
          border-radius: 4px 0 0 4px;
          border: 1px solid var(--divider-color);
        }
        
        .search-header select {
          padding: 8px;
          border: 1px solid var(--divider-color);
          border-left: none;
        }
        
        .search-header button {
          padding: 8px;
          background-color: var(--primary-color);
          color: white;
          border: none;
          border-radius: 0 4px 4px 0;
          cursor: pointer;
        }
        
        .loading {
          text-align: center;
          padding: 16px;
          font-style: italic;
        }
        
        .search-results {
          max-height: 50vh;
          overflow-y: auto;
        }
        
        .result-item {
          display: flex;
          align-items: center;
          padding: 8px;
          cursor: pointer;
          border-bottom: 1px solid var(--divider-color);
        }
        
        .result-item:hover {
          background-color: var(--secondary-background-color);
        }
        
        .result-item img {
          width: 50px;
          height: 50px;
          object-fit: cover;
          margin-right: 16px;
        }
        
        .item-info {
          flex-grow: 1;
        }
        
        .item-name {
          font-weight: bold;
        }
        
        .item-artist {
          font-size: 0.9em;
          color: var(--secondary-text-color);
        }
        
        .controls-container {
          padding: 16px;
        }
        
        .playback-controls {
          display: flex;
          justify-content: center;
          margin-bottom: 24px;
        }
        
        .playback-controls button {
          background: none;
          border: none;
          font-size: 24px;
          cursor: pointer;
          padding: 8px 16px;
          color: var(--primary-color);
        }
        
        .volume-controls {
          display: flex;
          align-items: center;
        }
        
        .volume-controls button {
          background: none;
          border: none;
          cursor: pointer;
          color: var(--primary-color);
        }
        
        .volume-controls input {
          flex-grow: 1;
          margin: 0 16px;
        }
      `;
    }
  }
  
  customElements.define("music-assistant-spotify-card", MusicAssistantSpotifyCard);
  
  window.customCards = window.customCards || [];
  window.customCards.push({
    type: "music-assistant-spotify-card",
    name: "Music Assistant Spotify Card",
    description: "Control Music Assistant speakers and play Spotify music",
  });