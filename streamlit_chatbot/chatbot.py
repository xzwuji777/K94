import streamlit as st
import google.generativeai as genai

# ========== CONFIG ==========
# Load Gemini API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")  # or gemini-1.5-pro

# ========== STATE INIT ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# ========== SONG SUGGESTION LOGIC ==========
def get_song_recommendations(user_message: str):
    prompt = (
        "You are a music recommender AI. "
        "The user will give you a genre, mood, or just type naturally about music. "
        "From their message, suggest 5 songs that match their request. "
        "Reply in a clean bullet-point list with only **song title – artist**."
        f"\n\nUser message: {user_message}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Failed to generate suggestions: {e}"

# ========== CHAT UI ==========
def chat_ui():
    st.subheader("🎵 Ask for Song Recommendations")

    initialize_session_state()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type anything about songs (e.g., 'sad pop', 'energetic kpop', 'I want relaxing jazz songs')")

    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get Gemini response
        reply = get_song_recommendations(user_input)

        # Display Gemini's reply
        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

# ========== MAIN ==========
def main():
    st.set_page_config(page_title="Gemini Music Chatbot 🎧", page_icon="🎶")
    st.title("🎶 Your Go-To Music")
    st.markdown("Just type any **genre, mood, or natural sentence** and get personalized music suggestions!")

    chat_ui()

if __name__ == "__main__":
    main()
