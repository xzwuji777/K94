import streamlit as st
import google.generativeai as genai

# ========== SETUP ==========
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# ========== SESSION STATE ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "song_suggestions" not in st.session_state:
        st.session_state.song_suggestions = []

# ========== GEMINI AI SONG SUGGESTION ==========
def get_songs_from_genre(genre):
    prompt = (
        f"Suggest 5 popular songs for the music genre '{genre}'. "
        "Provide only the song titles separated by commas."
    )
    response = model.generate_content(prompt)
    songs_text = response.text.strip()
    # Parse songs, split by comma and strip whitespace
    songs_list = [song.strip() for song in songs_text.split(",") if song.strip()]
    return songs_list

# ========== MUSIC RECOMMENDER UI ==========
def music_recommender():
    st.subheader("🎵 Music Recommendation")

    genre = st.text_input("Type a music genre to get song recommendations:")

    if genre:
        st.info(f"Fetching songs for genre: {genre} ...")
        songs = get_songs_from_genre(genre)

        if songs:
            st.session_state.song_suggestions = songs
            st.success(f"Here are some songs from the '{genre}' genre:")
            for idx, song in enumerate(songs, 1):
                st.write(f"{idx}. {song}")
                # Optional: if you have audio files named after songs, uncomment:
                # audio_path = f"streamlit_chatbot/songs/{song.split()[0].lower()}.mp3"
                # st.audio(audio_path)
        else:
            st.warning("No songs found for this genre.")

# ========== CHAT UI ==========
def chat_ui():
    st.subheader("💬 Chat with Us")
    initialize_session_state()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("What's on your mind?"):
        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        # Use Gemini AI to generate response
        response = model.generate_content(prompt).text
        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# ========== SIDEBAR ==========
def sidebar():
    with st.sidebar:
        st.title("📱 Follow Us")
        st.markdown("**Instagram**")
        st.markdown("**TikTok**")

# ========== MAIN ==========
def main():
    st.title("🎶 AI-Powered Music Recommender")

    initialize_session_state()
    sidebar()
    music_recommender()
    chat_ui()

if __name__ == "__main__":
    main()
