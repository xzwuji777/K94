# chatbot.py
import streamlit as st
import google.generativeai as genai

# ========== CONFIG ==========

# Load Gemini API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ========== STATE INIT ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# ========== SONG SUGGESTION LOGIC ==========
def get_songs_from_genre_and_mood(genre, mood):
    prompt = (
        f"Suggest 5 songs that fit the '{genre}' genre and a '{mood}' mood. "
        "List only the song titles and artists in a clean, bullet-point format."
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

    user_input = st.chat_input("Type a genre and mood (e.g., 'sad pop', 'energetic kpop')")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input})

        # Ask Gemini for song suggestions
        reply = get_songs_from_genre_and_mood(genre=user_input.split()[0], mood=" ".join(user_input.split()[1:]))

        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

# ========== MAIN ==========
def main():
    st.set_page_config(page_title="Gemini Music Chatbot 🎧", page_icon="🎶")
    st.title("🎶 Music Post")
    st.markdown("Just type a **genre + mood** and get personalized music suggestions!")

    chat_ui()
    import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit secrets
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

# Safety check: Stop app if key is missing
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .streamlit/secrets.toml.")
    st.stop()

# Configure Gemini client
genai.configure(api_key=GOOGLE_API_KEY)

# Use a valid model name — update to match available models
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")  # Example valid model

# Generate music suggestions
prompt = "Suggest 5 sad pop songs"
response = model.generate_content(prompt)

# Display suggestions
if hasattr(response, "text"):
    st.write("🎵 Music Suggestions:")
    st.write(response.text)
else:
    st.error("❌ Failed to generate suggestions. Please check model compatibility.")


if __name__ == "__main__":
    main()
