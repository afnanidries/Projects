import os
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# 🔍 Debug print to confirm correct redirect URI is loaded
print("🔎 SPOTIFY_REDIRECT_URI =", SPOTIFY_REDIRECT_URI)

def get_auth_url():
    scopes = "playlist-modify-private playlist-modify-public user-top-read"

    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={SPOTIFY_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={urllib.parse.quote(SPOTIFY_REDIRECT_URI)}"
        f"&scope={urllib.parse.quote(scopes)}"
        "&show_dialog=true"
    )
    return auth_url


def get_token(code):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(token_url, data=payload).json()
    return {
        "access_token": response.get("access_token"),
        "refresh_token": response.get("refresh_token"),
        "expires_in": response.get("expires_in")
    }


def refresh_access_token(refresh_token):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(token_url, data=payload).json()
    return response.get("access_token")


def get_user_profile(access_token):
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


def generate_music_playlist(duration_minutes, access_token):
    print(f"🕒 Trip duration (min): {duration_minutes}")
    print("🎶 Generating music playlist...")

    headers = {"Authorization": f"Bearer {access_token}"}
    target_ms = duration_minutes * 60000
    tolerance_ms = 30000
    min_ms = target_ms - tolerance_ms
    max_ms = target_ms + tolerance_ms

    top_target_ms = int(target_ms * 0.8)
    new_target_ms = target_ms - top_target_ms

    selected = []
    total_ms = 0

    # --- 1. Get user top tracks (~80%) ---
    top_url = "https://api.spotify.com/v1/me/top/tracks?limit=30&time_range=medium_term"
    top_res = requests.get(top_url, headers=headers)
    top_tracks = top_res.json().get("items", []) if top_res.status_code == 200 else []

    for t in top_tracks:
        uri = f"spotify:track:{t['id']}"
        duration_ms = t["duration_ms"]
        if uri not in [u for u, _ in selected]:
            selected.append((uri, duration_ms))
            total_ms += duration_ms
            if total_ms >= top_target_ms:
                break

    # --- 2. Add new releases (~20%) ---
    new_total = 0
    new_url = "https://api.spotify.com/v1/browse/new-releases?limit=10"
    new_res = requests.get(new_url, headers=headers)
    albums = new_res.json().get("albums", {}).get("items", []) if new_res.status_code == 200 else []

    for album in albums:
        album_id = album["id"]
        tracks_res = requests.get(f"https://api.spotify.com/v1/albums/{album_id}/tracks", headers=headers)
        tracks = tracks_res.json().get("items", []) if tracks_res.status_code == 200 else []
        for track in tracks:
            uri = f"spotify:track:{track['id']}"
            duration_ms = track.get("duration_ms", 200000)
            if uri not in [u for u, _ in selected]:
                selected.append((uri, duration_ms))
                new_total += duration_ms
                if new_total >= new_target_ms:
                    break
        if new_total >= new_target_ms:
            break

    print(f"📦 Collected total: {round(sum(d for _, d in selected) / 60000, 2)} min, {len(selected)} tracks")

    # --- 3. Create playlist ---
    user_id = requests.get("https://api.spotify.com/v1/me", headers=headers).json().get("id")
    playlist_data = {
        "name": f"TripTune Mixed ({duration_minutes} min)",
        "description": "Top + New Releases mix 🚗🎧",
        "public": True
    }
    playlist_res = requests.post(f"https://api.spotify.com/v1/users/{user_id}/playlists", headers=headers, json=playlist_data)
    if playlist_res.status_code != 201:
        print("❌ Failed to create playlist:", playlist_res.text)
        return None

    playlist_id = playlist_res.json()["id"]

    # --- 4. Trim and optimize track list ---
    selected.sort(key=lambda x: -x[1])  # Longest first
    final_tracks = []
    final_duration = 0

    for uri, dur in selected:
        if final_duration + dur <= max_ms:
            final_tracks.append(uri)
            final_duration += dur
            if final_duration >= min_ms:
                break

    print(f"🎯 Final trimmed playlist length: {round(final_duration / 60000, 2)} min, {len(final_tracks)} tracks")

    for i in range(0, len(final_tracks), 100):
        requests.post(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            headers=headers,
            json={"uris": final_tracks[i:i+100]}
        )

    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
    print(f"🎉 Created Playlist: {playlist_url}")
    return playlist_url
