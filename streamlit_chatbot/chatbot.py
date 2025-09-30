import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import io
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ========== SETUP ==========

# Gemini setup
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model_vision = genai.GenerativeModel("gemini-pro-vision")
model_text = genai.GenerativeModel("gemini-pro")

# Spotify setup (from .streamlit/secrets.toml)
SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = st.secrets["SPOTIFY_REDIRECT_URI"]

scope = "user-top-read"

# ========== SESSION STATE ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "suggested_songs" not in st.session_state:
        st.session_state.suggested_songs = []
    if "spotify_authenticated" not in st.session_state:
        st.session_state.spotify_authenticated = False
    if "top_artists" not in st.session_state:
        st.session_state.top_artists = []

# ========== CSS ==========
def apply_custom_css():
    st.markdown("""
        <style>
        .stChatMessage {
            background-color: #ffe5b4 !important;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .block-container {
            background-color: #fff7ec;
        }
        </style>
    """, unsafe_allow_html=True)

# ========== SPOTIFY AUTH ==========
def authenticate_spotify():
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope
    )

    token_info = sp_oauth.get_access_token(as_dict=True)
    if token_info:
        st.session_state.spotify_authenticated = True
        sp = spotipy.Spotify(auth=token_info["access_token"])

        # Get user's top 5 artists
        top_artists_data = sp.current_user_top_artists(limit=5)
        top_artists = [artist["name"] for artist in top_artists_data["items"]]
        st.session_state.top_artists = top_artists

        st.success(f"Authenticated! Top Artists: {', '.join(top_artists)}")
    else:
        auth_url = sp_oauth.get_authorize_url()
        st.markdown(f"[Click here to authenticate with Spotify]({auth_url})")

# ========== IMAGE UPLOAD + AI ==========
def image_uploader_and_ai():
    st.subheader("🖼️ Drop Your Post!")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your uploaded image", use_column_width=True)

        # Convert image to bytes
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        if not st.session_state.spotify_authenticated:
            st.warning("Please authenticate with Spotify first to personalize song recommendations.")
            return

        st.info("Analyzing image and matching with your top Spotify artists...")

        # Combine user artist preferences with image analysis
        artists = ", ".join(st.session_state.top_artists)
        prompt = (
            f"The user likes these artists: {artists}. "
            f"Based on this image, suggest 3 suitable songs that reflect the image mood and the user's music taste. "
            "Return only song titles. Keep it concise."
        )

        response = model_vision.generate_content([
            prompt,
            image_bytes
        ])

        # Parse and show suggestions
        suggested = response.text.strip().split("\n")
        st.session_state.suggested_songs = [s.strip("•- ") for s in suggested if s.strip()]
        st.success("Personalized songs generated!")

        for song in st.session_state.suggested_songs:
            st.write(f"🎵 {song}")

# ========== CHAT ==========
def chat_ui():
    st.subheader("💬 Chat with Us")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("What's on your mind?"):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = model_text.generate_content(prompt).text
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# ========== SIDEBAR ==========
def sidebar():
    with st.sidebar:
        st.title("📱 Follow Us")
        st.markdown("**Instagram**: @yourhandle")
        st.markdown("**TikTok**: @yourhandle")

# ========== MAIN ==========
def main():
    apply_custom_css()
    st.title("🎶 AI Song Suggestions Based on Your Image & Spotify")

    initialize_session_state()
    sidebar()

    if not st.session_state.spotify_authenticated:
        authenticate_spotify()
    else:
        st.success("Spotify account connected!")

    image_uploader_and_ai()
    chat_ui()

if __name__ == "__main__":
    main()
