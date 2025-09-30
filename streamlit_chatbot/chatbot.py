import streamlit as st
import google.generativeai as genai

# ========== CONFIG ==========
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Pick a reliable Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")

# ========== STATE INIT ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# ========== SONG SUGGESTION LOGIC ==========
def get_song_recommendations(user_message: str):
    """
    Generate 5 song suggestions as a Python list.
    """
    prompt = (
        "You are a professional music recommender AI.\n"
        "The user will provide a genre, mood, or both (e.g., 'sad pop', 'energetic kpop').\n"
        "Your job:\n"
        "1. Detect the genre and mood.\n"
        "2. Suggest exactly 5 songs.\n"
        "3. Output strictly as a Python list of strings, formatted like this:\n"
        "   [\"Song – Artist\", \"Song – Artist\", \"Song – Artist\", \"Song – Artist\", \"Song – Artist\"]\n"
        "No extra text, no explanations.\n\n"
        f"User request: {user_message}"
    )

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            text = response.text.strip()
            # Try to safely evaluate Gemini's output into a Python list
            try:
                songs = eval(text)
                if isinstance(songs, list):
                    return songs
            except Exception:
                # fallback: split lines if it's not a proper list
                return [line.strip("-• ") for line in text.split("\n") if line.strip()]
        return []
    except Exception as e:
        return [f"❌ Error: {str(e)}"]

# ========== CHAT UI ==========
def chat_ui():
    st.subheader("🎵 Genre & Mood-Based Song Recommendations")

    initialize_session_state()

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if isinstance(msg["content"], list):
                for song in msg["content"]:
                    st.write(f"- {song}")
            else:
                st.write(msg["content"])

    # User input
    user_input = st.chat_input("Type a genre & mood (e.g., 'happy indie', 'dark rap', 'chill lo-fi')")

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get Gemini response
        songs = get_song_recommendations(user_input)

        # Show assistant message
        with st.chat_message("assistant"):
            for song in songs:
                st.write(f"- {song}")
        st.session_state.messages.append({"role": "assistant", "content": songs})

# ========== MAIN ==========
def main():
    st.set_page_config(page_title="Gemini Music Chatbot 🎧", page_icon="🎶")
    st.title("🎶 Mood & Genre-Based Music Recommender")
    st.markdown("Get **5 personalized song suggestions** as a clean list format!")

    chat_ui()

if __name__ == "__main__":
    main()
