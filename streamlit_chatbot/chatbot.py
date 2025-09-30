import streamlit as st
import google.generativeai as genai

# ========== CONFIG ==========
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Pick a reliable Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# ========== STATE INIT ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# ========== SONG SUGGESTION LOGIC ==========
def get_song_recommendations(user_message: str):
    """
    Generate 5 song suggestions tailored to user's requested genre and/or mood.
    """
    prompt = (
        "You are a professional music recommender AI.\n"
        "The user will provide a **genre, mood, or both** (e.g., 'sad pop', 'energetic kpop', 'relaxing jazz').\n"
        "Your task:\n"
        "1. Analyze the user's input to detect the genre and mood.\n"
        "2. Suggest exactly 5 songs that best match that request.\n"
        "3. Output only in this format:\n"
        "   - Song Title – Artist\n"
        "\n"
        f"User request: {user_message}"
    )

    try:
        response = model.generate_content(prompt)

        # Debug: show full response if needed
        # st.write(response)

        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return "⚠️ I couldn’t generate song suggestions. Try rephrasing!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ========== CHAT UI ==========
def chat_ui():
    st.subheader("🎵 Genre & Mood-Based Song Recommendations")

    initialize_session_state()

    # Display conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    user_input = st.chat_input("Type a genre & mood (e.g., 'happy indie', 'dark rap', 'chill lo-fi')")

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get Gemini response
        reply = get_song_recommendations(user_input)

        # Show assistant message
        with st.chat_message("assistant"):
            st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ========== MAIN ==========
def main():
    st.set_page_config(page_title="Gemini Music Chatbot 🎧", page_icon="🎶")
    st.title("🎶 Mood & Genre-Based Music Recommender")
    st.markdown("Get **5 personalized song suggestions** based on your mood and genre request!")

    chat_ui()

if __name__ == "__main__":
    main()
