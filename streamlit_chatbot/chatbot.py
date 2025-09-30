import streamlit as st
import google.generativeai as genai

# ========== CONFIG ==========
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # fallback if 2.5 isn't available

# ========== STATE INIT ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# ========== SONG SUGGESTION LOGIC ==========
def get_song_recommendations(user_message: str):
    # Build conversation history for context
    conversation = ""
    for msg in st.session_state.messages[-5:]:  # keep last 5 exchanges
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"
    
    prompt = (
        "You are a music recommender AI. "
        "The user may ask by genre, mood, or natural text. "
        "Suggest 5 songs that match their request. "
        "Format: bullet-point list with only **song title – artist**.\n\n"
        f"{conversation}\nUser: {user_message}"
    )

    try:
        response = model.generate_content(prompt)
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        elif response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        else:
            return "⚠️ I couldn’t generate a response this time. Try again!"
    except Exception as e:
        return "❌ Something went wrong while fetching song suggestions."

# ========== CHAT UI ==========
def chat_ui():
    st.subheader("🎵 Ask for Song Recommendations")

    initialize_session_state()

    # Render past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type anything about songs (e.g., 'sad pop', 'energetic kpop', 'I want relaxing jazz songs')")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input})

        reply = get_song_recommendations(user_input)

        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

# ========== MAIN ==========
def main():
    st.set_page_config(page_title="Gemini Music Chatbot 🎧", page_icon="🎶")
    st.title("🎶 Your Go-To Music")
    st.markdown("Type any **genre, mood, or natural sentence** and get personalized music suggestions!")

    chat_ui()

if __name__ == "__main__":
    main()
