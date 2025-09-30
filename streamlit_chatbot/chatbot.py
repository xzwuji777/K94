import streamlit as st
import random
from PIL import Image
import google.generativeai as genai

# ========== SETUP ==========
# Configure API key for Gemini
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Initialize session state for chat
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Music suggestions by genre
songs = {
    'ballad': ['odoriko', 'labyrinth by taylor swift', 'cause you have to by lany'],
    'kpop': ['tempo by exo', 'song E', 'song F'],
    'hiphop': ['apt', 'song H', 'song I'],
    'pop-punk': ['not ok by 5sos', 'no choice by fly by midnight', 'song L'],
    'galau': ['mjol', 'song Y', 'song Z']
}

# ========== MUSIC SUGGESTION ==========
def music_recommender():
    st.subheader("🎵 Music Recommendation")
    genre = st.selectbox("Choose your music genre", list(songs.keys()))
    
    suggestion_index = 0
    suggestions = songs[genre]
    
    while suggestion_index < len(suggestions):
        song = suggestions[suggestion_index]
        st.write(f"How about choosing **{song}**?")
        
        audio_file = f"streamlit_chatbot/songs/{song.split()[0].lower()}.mp3"
        st.audio(audio_file)
        
        taste = st.selectbox("Is it to your music taste?", ['yes', 'no'], key=f"taste_{suggestion_index}")
        
        if taste == 'yes':
            st.success("Glad you liked it! 🎶")
            break
        else:
            suggestion_index += 1
    
    if suggestion_index == len(suggestions):
        st.warning("No more suggestions in this genre!")

# ========== POST IMAGE ==========
def image_uploader():
    st.subheader("🖼️ Drop Your Post!")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your uploaded image", use_column_width=True)

# ========== CHAT ==========
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

        response = f"You said: {prompt}"
        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# ========== SIDEBAR ==========
def sidebar():
    with st.sidebar:
        st.title("📱 Follow Us")
        st.markdown("**Instagram**")
        st.markdown("**TikTok**")

# ========== MAIN APP ==========
def main():
    st.title("🎶 Music Post App")

    sidebar()
    image_uploader()
    music_recommender()
    chat_ui()

if __name__ == "__main__":
    main()
