import streamlit as st
import google.generativeai as genai
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import urllib.parse

# ========== CONFIG & AUTH ==========

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = st.secrets["SPOTIFY_REDIRECT_URI"]

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-pro")  # adjusted model name

# Configure Spotify client (client credentials for search)
spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# ========== FUNCTIONS ==========

def get_songs_from_genre_and_mood(genre: str, mood: str) -> list[str]:
    """
    Ask Gemini to suggest songs (title + artist) based on genre and mood.
    """
    prompt = (
        f"Suggest 5 songs (title + artist) that match the genre '{genre}' "
        f"and the mood '{mood}'. Return them in a comma-separated format like:\n"
        "Title1 — Artist1, Title2 — Artist2, ..."
    )
    try:
        resp = model.generate_content(prompt)
        text = resp.text.strip()
        # Split by comma, parse title and artist
        items = [it.strip() for it in text.split(",") if it.strip()]
        return items
    except Exception as e:
        st.error("❌ Gemini AI error:")
        st.exception(e)
        return []

def spotify_search_track(query: str):
    """
    Search Spotify track, return first match metadata (preview_url, external url)
    """
    try:
        results = spotify.search(q=query, type="track", limit=1)
        items = results.get("tracks", {}).get("items", [])
        if items:
            track = items[0]
            return {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "preview_url": track.get("preview_url"),
                "spotify_url": track["external_urls"]["spotify"]
            }
    except Exception as e:
        st.warning(f"Spotify search failed for {query}: {e}")
    return None

def youtube_embed_url(song: str, artist: str) -> str:
    """
    Return YouTube search link or embed link fallback
    """
    # simplified: open search on YouTube
    query = urllib.parse.quote_plus(f"{song} {artist}")
    return f"https://www.youtube.com/results?search_query={query}"

# ========== STREAMLIT UI ==========

st.set_page_config(page_title="🎶 Gemini + Spotify Music Recommender", page_icon="🎧")
st.title("AI Song Recommender (Genre + Mood)")

genre = st.text_input("🎸 Enter music genre (e.g. pop, jazz, rock):")
mood = st.text_input("🎭 Enter mood (e.g. happy, sad, energetic):")

if st.button("Recommend Songs"):
    if not genre or not mood:
        st.warning("Please enter both genre and mood.")
    else:
        with st.spinner("🎵 Generating suggestions..."):
            suggestions = get_songs_from_genre_and_mood(genre, mood)
        if suggestions:
            st.subheader("🎯 Suggested Songs & Previews")
            for i, item in enumerate(suggestions, start=1):
                # item should be "Title — Artist"
                parts = item.split("—")
                if len(parts) == 2:
                    song = parts[0].strip()
                    artist = parts[1].strip()
                else:
                    # fallback if format is different
                    song = item
                    artist = ""
                st.markdown(f"**{i}. {song} — {artist}**")

                # Search Spotify
                track = spotify_search_track(f"{song} {artist}")
                if track:
                    if track["preview_url"]:
                        st.audio(track["preview_url"])
                    st.markdown(f"[Open in Spotify]({track['spotify_url']})")
                else:
                    # fallback to YouTube search link
                    yt = youtube_embed_url(song, artist)
                    st.markdown(f"[YouTube search]({yt})")
        else:
            st.warning("No song suggestions returned. Try different inputs.")
