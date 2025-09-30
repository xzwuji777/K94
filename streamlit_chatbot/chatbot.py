import streamlit as st
import google.generativeai as genai
model = genai.GenerativeModel("gemini-pro")  # for text
import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("Suggest 5 sad pop songs")
suggestions = response.text  # This is important
prompt = "Suggest 5 upbeat K-pop songs suitable for a gym workout."


# ========== SETUP ==========
# Load Gemini API key from secrets
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .streamlit/secrets.toml.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Load the Gemini model
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("❌ Failed to load Gemini model.")
    st.exception(e)
    st.stop()

# ========== APP TITLE ==========
st.set_page_config(page_title="🎵 AI Mood & Genre Music Recommender")
st.title("🎶 AI Music Recommender by Genre & Mood")

# ========== USER INPUT ==========
genre = st.text_input("🎧 Enter a music genre (e.g., pop, jazz, hip hop):")
mood = st.text_input("😊 Enter a mood (e.g., happy, sad, relaxed, energetic):")

# ========== GET RECOMMENDATIONS ==========
def get_song_suggestions(genre, mood):
    prompt = (
        f"Suggest 5 songs that match the music genre '{genre}' "
        f"and the mood '{mood}'. Return only the song titles with artist names, as a bullet list."
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error("⚠️ Gemini API failed to respond.")
        st.exception(e)
        return ""

# ========== DISPLAY RESULTS ==========
if genre and mood:
    with st.spinner("Finding songs for your vibe... 🎶"):
        suggestions = get_song_suggestions(genre, mood)

    if suggestions:
        st.subheader("🎵 Suggested Songs:")
        st.markdown(suggestions)
    else:
        st.warning("No suggestions found. Try a different genre or mood.")
else:
    st.info("Enter both a genre and mood to get started.")
