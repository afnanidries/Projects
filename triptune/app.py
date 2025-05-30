from flask import Flask, render_template, request, redirect, url_for, session
from utils.route_api import get_trip_duration
from utils.spotify_api import (
    get_auth_url,
    get_token,
    refresh_access_token,
    generate_music_playlist
)
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-key")

# Optional for debugging session on Render (esp. if HTTPS is off)
app.config.update(
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE='Lax'
)

@app.route('/login')
def login():
    print("🔐 Redirecting to Spotify login...")
    return redirect(get_auth_url())


@app.route('/callback')
def callback():
    code = request.args.get("code")
    print("🎯 /callback hit. Received code:", code)

    if not code:
        print("❌ No code received in callback.")
        return "Authorization failed.", 400

    token_data = get_token(code)
    print("🔐 Token data received:", token_data)

    session["access_token"] = token_data.get("access_token")
    session["refresh_token"] = token_data.get("refresh_token")
    print("✅ Tokens saved in session.")
    
    return redirect(url_for("index"))


@app.route('/', methods=['GET', 'POST'])
def index():
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")

    print("DEBUG: access_token =", access_token)
    print("DEBUG: refresh_token =", refresh_token)

    if not access_token:
        print("⚠️ No access token. Prompting login.")
        return render_template('index.html', playlist_url=None, login_required=True)

    # Check if token is still valid
    test_auth = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {access_token}"})
    if test_auth.status_code == 401 and refresh_token:
        print("🔄 Refreshing expired access token...")
        new_access_token = refresh_access_token(refresh_token)
        session["access_token"] = new_access_token
        access_token = new_access_token
        print("✅ Access token refreshed.")

    if request.method == 'POST':
        try:
            start_location = request.form['start']
            end_location = request.form['end']

            print("📍 Start:", start_location, "| End:", end_location)
            duration = get_trip_duration(start_location, end_location)
            print("🕒 Trip duration (min):", duration)

            if duration is None:
                print("⚠️ Could not calculate trip duration.")
                return render_template('index.html', playlist_url=None, login_required=False)

            playlist_url = generate_music_playlist(duration, access_token)
            print("✅ Playlist URL:", playlist_url)

            return render_template('index.html', playlist_url=playlist_url)
        except Exception as e:
            print("❌ Error during playlist generation:", e)
            return render_template('index.html', playlist_url=None)

    return render_template('index.html', playlist_url=None)


# # Local-only runner (not needed for Render with Gunicorn)
# if __name__ == '__main__':
#     app.run(debug=True)
