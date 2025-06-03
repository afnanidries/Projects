# 🎵 TripTune – Spotify Playlist Generator Based on Trip Duration

**TripTune** is an AI-inspired web application that creates the perfect-length Spotify playlist for your road trip. Simply enter your start and end locations, log in with Spotify, and get a playlist that ends *right as you arrive*. No skipped vibes. No awkward silences.

---

## 🚀 Live Demo  
🌐 [https://triptune.onrender.com](https://triptune.onrender.com)

---

## Features

- **Trip Duration Integration**  
  Uses the Google Maps API to calculate exact trip time between two locations.

- **Spotify OAuth Login**  
  Authenticates the user to fetch top tracks and personalize the playlist.

- **Intelligent Playlist Construction**  
  - Pulls your top 30 Spotify tracks  
  - Adds 1–2 newly released tracks for freshness  
  - Filters and arranges songs to match your trip time (±30 seconds)

- **Token Refresh Logic**  
  Automatically refreshes expired Spotify access tokens during session.

- **Deployed on Render**  
  Lightweight Flask backend + HTML templates, no frontend framework required.

---

## Tech Stack

- **Backend:** Python, Flask  
- **APIs:** Spotify Web API, Google Maps Distance Matrix API  
- **Auth:** OAuth2.0 (Spotify)  
- **Deployment:** Render  
- **Templating:** Jinja2 + HTML/CSS  
- **Session Management:** Flask sessions with token refresh

---

## 📸 Screenshots

| Page                              | Description                                                             |
|-----------------------------------|-------------------------------------------------------------------------|
| ![Landing Page](screenshots/landing-page.png)     | Homepage with TripTune branding and trip input form                    |
| ![Login Page](screenshots/login-page.png)         | Spotify login prompt via OAuth                                         |
| ![Spotify Auth Page](screenshots/spotify-auth.png)| Spotify’s authorization screen for granting playlist + top tracks access |
| ![Playlist Result Page](screenshots/playlist-result.png) | Generated playlist link with timing confirmation                      |
| ![Mobile View](screenshots/mobile-view.png)       | Responsive view of the app on a mobile browser                         |

---

## File Structure

```
triptune/
├── app.py                # Flask app entry point
├── utils/
│   ├── route_api.py      # Trip duration via Google Maps API
│   └── spotify_api.py    # Spotify auth & playlist logic
├── templates/
│   └── index.html        # UI layout
├── static/               # (Optional) CSS/images
├── requirements.txt      # Python dependencies
└── Procfile              # For Render deployment
```

---

## Try It Yourself

### You'll Need:
- A Spotify Developer Account → [https://developer.spotify.com](https://developer.spotify.com)
- A Google Maps API key
- A Render account for deployment (or run locally)

### Local Setup:
```bash
git clone https://github.com/afnanidries/Projects.git
cd Projects/triptune

# Set your env variables
touch .env
# Add the following keys inside:
# SPOTIFY_CLIENT_ID=your_id
# SPOTIFY_CLIENT_SECRET=your_secret
# SPOTIFY_REDIRECT_URI=https://triptune.onrender.com/callback (or http://localhost:5000/callback)
# GOOGLE_MAPS_API_KEY=your_maps_key
# FLASK_SECRET=your_flask_secret

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

---

## Development Decisions & Challenges

- **Mood Matching with Audio Features**  
  Originally planned to let users choose a mood for the entire trip (e.g. "chill", "hype", "melancholy") or even set the desired mood of the *final* song. However, Spotify's older audio feature endpoints (used in `recommendations`) have been deprecated, making this infeasible for public use without stable support.

- **Recommendation API Limitations**  
  I considered using Spotify’s global recommendation system to blend in new music, but without user-specific seeding and with limitations in the current `/recommendations` endpoint, it didn’t scale well or match playlist durations precisely. The final implementation prioritizes top tracks and new releases to achieve a reliable and timely playlist.

- **Apple Music Alternative**  
  Evaluated Apple Music for cross-platform support, but Spotify's API was more complete, offered better developer tooling, and had broader adoption — making it the more efficient choice for an MVP.

- **Podcasts and Audiobooks**  
  Wanted to include podcast or audiobook options, but Spotify’s API requires track or show IDs to queue non-music content — which can’t be pulled dynamically for new or public lists. Since I could only use content from the user’s listening history, this was removed from the core feature set for now.

- **Deployment Tradeoffs**  
  Chose Render for its ease of setup, free tier, and seamless integration with Flask. The app is session-based and refreshes Spotify tokens in the background to support longer use without re-authentication.

---

## About the Author

**Afnan Idries**  
📍 Durham, NC  
📧 afnanidries@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/afnanidries)  
🔗 [GitHub](https://github.com/afnanidries)

---

> Built as a personal project to combine maps, music, and mood — with an emphasis on end-to-end engineering, real-world APIs, and user delight.
