import os
from utils.spotify_api import search_lyrics_url, extract_lyrics, classify_lyrics_vibe

# Test songs: Includes a wider emotional range
test_tracks = [
    {"title": "My All", "artist": "Polo G"},                         # heartbreak
    {"title": "Bad (Remix)", "artist": "Wale"},                      # romantic
    {"title": "Coffee (Don't Read Signs)", "artist": "Odeal"},      # romantic
    {"title": "Heart Of A Woman", "artist": "Summer Walker"},       # romantic
    {"title": "Someone Like You", "artist": "Adele"},               # heartbreak
    {"title": "Don't Start Now", "artist": "Dua Lipa"},             # energetic
    {"title": "Shivers", "artist": "Ed Sheeran"},                   # romantic
    {"title": "Stay", "artist": "The Kid LAROI & Justin Bieber"},   # sad / heartbreak
    {"title": "Happy", "artist": "Pharrell Williams"},              # happy
    {"title": "Lose Yourself", "artist": "Eminem"}                  # energetic / angry
]

for track in test_tracks:
    print(f"\n🔍 Testing: {track['title']} by {track['artist']}")

    genius_url = search_lyrics_url(track['title'], track['artist'])
    print(f"🔗 Genius URL: {genius_url}")

    if not genius_url:
        print("❌ No lyrics page found.")
        continue

    lyrics = extract_lyrics(genius_url)
    if not lyrics:
        print("❌ No lyrics extracted.")
        continue

    print("📄 First 200 characters of lyrics:")
    print(lyrics[:200])

    mood = classify_lyrics_vibe(lyrics)
    print(f"🧠 Predicted mood: {mood}")
