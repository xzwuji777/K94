import streamlit as st
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== CONFIG ==========
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Spotify Auth
sp_oauth = SpotifyOAuth(
    client_id=st.secrets["spotify"]["CLIENT_ID"],
    client_secret=st.secrets["spotify"]["CLIENT_SECRET"],
    redirect_uri=st.secrets["spotify"]["REDIRECT_URI"],
    scope="user-top-read user-read-recently-played"
)

# ========== STATE INIT ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "spotify_token" not in st.session_state:
        st.session_state.spotify_token = None

# ========== SPOTIFY HELPERS ==========
def get_spotify_data():
    """Fetch user’s top artists and tracks if authenticated."""
    if not st.session_state.spotify_token:
        return None

    sp = spotipy.Spotify(auth=st.session_state.spotify_token)

    # Get top tracks
    top_tracks = sp.current_user_top_tracks(limit=5, time_range="short_term")
    top_tracks_list = [f"{t['name']} – {t['artists'][0]['name']}" for t in top_tracks['items']]

    # Get top artists
    top_artists = sp.current_user_top_artists(limit=5, time_range="short_term")
    top_artists_list = [a["name"] for a in top_artists["items"]]

    return {
        "top_tracks": top_tracks_list,
        "top_artists": top_artists_list
    }

# ========== GEMINI LOGIC ==========
def get_song_recommendations(user_message: str, spotify_data=None):
    conversation = ""
    for msg in st.session_state.messages[-5:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"

    spotify_context = ""
    if spotify_data:
        spotify_context = (
            f"\nThe user’s favorite artists are: {', '.join(spotify_data['top_artists'])}. "
            f"Their top recent tracks are: {', '.join(spotify_data['top_tracks'])}."
        )

    prompt = (
        "You are a personalized music recommender AI. "
        "The user may ask for genres, moods, or just describe music naturally. "
        "You MUST consider both their request and their Spotify preferences when recommending. "
        "Suggest 5 songs, format: bullet-point list **Song – Artist**.\n\n"
        f"{conversation}\nUser: {user_message}{spotify_context}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "⚠️ No response generated."
    except Exception:
        return "❌ Something went wrong while fetching recommendations."

# ========== CHAT UI ==========
def chat_ui():
    st.subheader("🎵 Ask for Song Recommendations (Personalized with Spotify)")

    initialize_session_state()

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Spotify login button
    if not st.session_state.spotify_token:
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"[🔗 Connect Spotify]({auth_url})")
        query_params = st.query_params

        # Capture token after redirect
        if "code" in query_params:
            token_info = sp_oauth.get_access_token(query_params["code"])
            st.session_state.spotify_token = token_info["access_token"]
            st.success("✅ Connected to Spotify! Refresh page.")
            st.rerun()
        return

    # User input
    user_input = st.chat_input("Type anything about songs (e.g., 'sad pop', 'energetic kpop')")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        spotify_data = get_spotify_data()
        reply = get_song_recommendations(user_input, spotify_data)

        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

# ========== MAIN ==========
def main():
    st.set_page_config(page_title="Gemini Music Chatbot 🎧", page_icon="🎶")
    st.title("🎶 Personalized AI Music Recommender")
    st.markdown("Get **AI-powered song suggestions** tailored to your Spotify taste!")

    chat_ui()

if __name__ == "__main__":
    main()
