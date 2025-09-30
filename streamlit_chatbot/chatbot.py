import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
import io

# ========== SETUP ==========
# Configure API key for Gemini
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model_vision = genai.GenerativeModel("gemini-pro-vision")
model_text = genai.GenerativeModel("gemini-pro")

# ========== INIT SESSION ==========
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "suggested_songs" not in st.session_state:
        st.session_state.suggested_songs = []

# ========== CSS STYLING ==========
def apply_custom_css():
    st.markdown(
        """
        <style>
            .stChatMessage {
                background-color: #ffe5b4 !important;  /* Peach color */
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# ========== IMAGE UPLOADER WITH AI ==========
def image_uploader_and_ai():
    st.subheader("🖼️ Drop Your Post!")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your uploaded image", use_column_width=True)

        # Convert image to bytes
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        # Ask Gemini to suggest songs based on the image
        st.info("Analyzing image and generating song suggestions...")

        prompt = "Based on this image, suggest 3 suitable song titles. Keep it short."

        response = model_vision.generate_content([
            prompt,
            image_bytes
        ])

        # Store and display suggested songs
        suggested = response.text.strip().split("\n")
        st.session_state.suggested_songs = [s.strip("•- ") for s in suggested if s.strip()]
        st.success("Songs generated based on image!")

        for song in st.session_state.suggested_songs:
            st.write(f"- 🎵 {song}")

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

        # Get response from Gemini
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
    st.title("🎶 Music Post App with AI")

    sidebar()
    image_uploader_and_ai()
    chat_ui()

if __name__ == "__main__":
    main()
