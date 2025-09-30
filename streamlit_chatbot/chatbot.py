import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse

# ========== CONFIG ==========
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

CLIENT_ID = st.secrets["spotify"]["CLIENT_ID"]
CLIENT_SECRET = st.secrets["spotify"]["CLIENT_SECRET"]
REDIRECT_URI = st.secrets["spotify"]["REDIRECT_URI"]

# ✅ Step 4: Debug secrets to ensure they load correctly
st.write("🔑 Client ID loaded:", CLIENT_ID[:10] + "...")
st.write("🌍 Redirect URI loaded:", REDIRECT_URI)

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-top-read user-read-recently-played user-read-email"
)

# ========== STATE ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = None

# ========== SPOTIFY HELPERS ==========
def get_spotify_data():
    """Fetch top artists and tracks for personalization."""
    if not st.session_state.spotify_token:
        return None

    sp = spotipy.Spotify(auth=st.session_state.spotify_token)
    top_tracks = sp.current_user_top_tracks(limit=5, time_range="short_term")
    top_artists = sp.current_user_top_artists(limit=5, time_range="short_term")

    return {
        "top_tracks": [f"{t['name']} – {t['artists'][0]['name']}" for t in top_tracks["items"]],
        "top_artists": [a["name"] for a in top_artists["items"]],
    }

def search_spotify_track(track_name, artist):
    """Search track on Spotify and return a Spotify URL if found."""
    try:
        sp = spotipy.Spotify(auth=st.session_state.spotify_token)
        query = f"{track_name} {artist}"
        results = sp.search(q=query, type="track", limit=1)
        if results["tracks"]["items"]:
            return results["tracks"]["items"][0]["external_urls"]["spotify"]
    except Exception:
        return None
    return None

def get_youtube_search_url(song):
    """Fallback: return a YouTube search link if no Spotify link is found."""
    query = urllib.parse.quote(song)
    return f"https://www.youtube.com/results?search_query={query}"

# ========== GEMINI LOGIC ==========
def get_song_recommendations(user_message: str, spotify_data=None):
    """Use Gemini to recommend songs based on user input + Spotify taste."""
    spotify_context = ""
    if spotify_data:
        spotify_context = (
            f"\nThe user’s favorite artists: {', '.join(spotify_data['top_artists'])}. "
            f"Their top tracks: {', '.join(spotify_data['top_tracks'])}."
        )

    prompt = (
        "You are a personalized music recommender AI. "
        "The user may ask for genres, moods, or just describe music naturally. "
        "You MUST consider both their request and their Spotify preferences. "
        "Suggest 5 songs. Reply ONLY in clean bullet-point list: Song – Artist.\n\n"
        f"User: {user_message}{spotify_context}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip().split("\n")
    except Exception:
        return []

# ========== CHAT UI ==========
def chat_ui():
    st.subheader("🎵 Go-To Music (Spotify + AI)")

    # Display conversation so far
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if not st.session_state.spotify_token:
        # Step 1: Show login button
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"[🔗 Connect Spotify]({auth_url})")

        # Step 3: Handle token exchange
        query_params = st.query_params
        if "code" in query_params:
            try:
                token_info = sp_oauth.get_access_token(query_params["code"], as_dict=True)
                st.session_state.spotify_token = token_info["access_token"]

                st.success("✅ Connected to Spotify! Refresh the page.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Token exchange failed: {e}")
        return

    # Step 2: Chat after Spotify connected
    user_input = st.chat_input("Type your music request (e.g., 'upbeat study songs', 'sad pop', 'relaxing jazz')")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get Spotify data + Gemini recommendations
        spotify_data = get_spotify_data()
        recommendations = get_song_recommendations(user_input, spotify_data)

        # Show recommendations with Spotify/YouTube links
        reply_links = []
        for rec in recommendations:
            if "–" in rec:
                song, artist = [x.strip() for x in rec.split("–", 1)]
                spotify_url = search_spotify_track(song, artist)
                if spotify_url:
                    reply_links.append(f"- [{rec}]({spotify_url})")
                else:
                    yt_url = get_youtube_search_url(rec)
                    reply_links.append(f"- [{rec}]({yt_url})")
            else:
                reply_links.append(f"- {rec}")

        reply_text = "\n".join(reply_links)

        with st.chat_message("assistant"):
            st.markdown(reply_text)

        st.session_state.messages.append({"role": "assistant", "content": reply_text})

# ========== MAIN ==========
def main():
    st.set_page_config(page_title="Gemini Music Chatbot 🎧", page_icon="🎶")
    st.title("🎶 Personalized AI Music Recommender")
    st.markdown("Get **AI-powered song suggestions** tailored to your Spotify taste, with clickable links!")

    chat_ui()

if __name__ == "__main__":
    main()
