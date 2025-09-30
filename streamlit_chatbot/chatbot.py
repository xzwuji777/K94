import streamlit as st
import google.generativeai as genai

# ========== SETUP ==========
# Load your Gemini API key securely from secrets
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")

# Safety check: If key not found, stop app
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .streamlit/secrets.toml.")
    st.stop()

# Configure the Gemini client
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini model (text-only)
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("❌ Failed to load Gemini model.")
    st.exception(e)
    st.stop()

# ========== SESSION STATE ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "song_suggestions" not in st.session_state:
        st.session_state.song_suggestions = []

# ========== GET SONG SUGGESTIONS ==========
def get_songs_from_genre(genre):
    prompt = (
        f"Suggest 5 popular songs for the music genre '{genre}'. "
        "Provide only the song titles, separated by commas."
    )

    try:
        response = model.generate_content(prompt)
        songs_text = response.text.strip()
        songs = [s.strip() for s in songs_text.split(",") if s.strip()]
        return songs
    except Exception as e:
        st.error("⚠️ Could not get song suggestions.")
        st.exception(e)
        return []

# ========== MUSIC RECOMMENDER ==========
def music_recommender():
    st.subheader("🎵 AI Song Recommendations")
    genre = st.text_input("🎧 Enter a music genre (e.g., pop, hip hop, jazz):")

    if genre:
        with st.spinner(f"Finding songs for genre: {genre}..."):
            songs = get_songs_from_genre(genre)

        if songs:
            st.success("✅ Songs found!")
            for idx, song in enumerate(songs, 1):
                st.write(f"{idx}. {song}")
        else:
            st.warning("😕 No songs returned. Try a different genre.")

# ========== CHAT INTERFACE ==========
def chat_ui():
    st.subheader("💬 Ask Anything (Gemini Chatbot)")
    initialize_session_state()

    # Show previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Handle user input
    user_input = st.chat_input("Type your question...")
    if user_input:
        # Display user message
        st.chat_message("user").write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate Gemini response
        try:
            ai_response = model.generate_content(user_input).text
        except Exception as e:
            ai_response = "⚠️ Gemini AI could not generate a response."
            st.error("Gemini error:")
            st.exception(e)

        # Display assistant response
        st.chat_message("assistant").write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# ========== SIDEBAR ==========
def sidebar():
    with st.sidebar:
        st.title("📱 Connect With Us")
        st.markdown("- Instagram: [@yourhandle](https://instagram.com)")
        st.markdown("- TikTok: [@yourhandle](https://tiktok.com)")

# ========== MAIN APP ==========
def main():
    st.set_page_config(page_title="AI Music Chatbot", page_icon="🎶")
    st.title("🎶 Gemini AI Music Chatbot")

    initialize_session_state()
    sidebar()
    music_recommender()
    chat_ui()

if __name__ == "__main__":
    main()
