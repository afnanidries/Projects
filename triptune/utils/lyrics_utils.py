import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# API keys
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI client setup
client = OpenAI(api_key=OPENAI_API_KEY)

def search_lyrics_url(song_title, artist):
    """
    Searches Genius API for the most relevant lyrics page URL.
    """
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    search_url = "https://api.genius.com/search"
    params = {"q": f"{song_title} {artist}"}
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"⚠️ Genius API error: {response.status_code}")
        return None

    hits = response.json().get("response", {}).get("hits", [])
    for hit in hits:
        if artist.lower() in hit["result"]["primary_artist"]["name"].lower():
            return hit["result"]["url"]
    return None

def extract_lyrics(genius_url):
    """
    Extracts lyrics from a Genius song page by scraping the HTML.
    """
    try:
        response = requests.get(genius_url)
        if response.status_code != 200:
            print(f"⚠️ Genius page error: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Genius uses <div> with class starting with 'Lyrics__Container'
        lyrics_divs = soup.find_all("div", class_=lambda c: c and c.startswith("Lyrics__Container"))

        lyrics = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs if div.get_text())
        return lyrics or None

    except Exception as e:
        print(f"❌ Error scraping lyrics: {e}")
        return None

def classify_lyrics_vibe(lyrics):
    if not lyrics or len(lyrics.strip()) == 0:
        return "unknown"

    try:
        prompt = (
            "Classify the overall emotional *mood* of the following song lyrics as one of these: "
            "happy, sad, chill, energetic, romantic, angry, heartbreak, or unknown. "
            "Only respond with the category.\n\n"
            f"Lyrics:\n{lyrics[:1000]}\n\nMood:"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You classify moods of song lyrics."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=10
        )

        content = response.choices[0].message.content.strip().lower()
        print(f"🧠 GPT Mood Raw Output: {content}")
        for mood in ["happy", "sad", "chill", "energetic", "romantic", "angry", "heartbreak"]:
            if mood in content:
                return mood
        return "unknown"

    except Exception as e:
        print("❌ OpenAI error:", e)
        return "unknown"

