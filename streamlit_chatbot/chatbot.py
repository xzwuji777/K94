


import streamlit as st
from PIL import Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image file
    image = Image.open(uploaded_file)

    # Display the image
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # You can also use the image data for processing here
    st.write("Image successfully uploaded and displayed!")
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Add simple bot response
        response = f"You said: {prompt}"
        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
with st.sidebar:
   st.title("Instagram")
   st.title("Tiktok")

if __name__ == "__main__":
    main()
def main():
 
 st.selectbox("music genre of choice", ["ballad", "kpop", "hiphop", "pop-punk", "galau"], index=0)
import streamlit as st
from PIL import Image

st.header("Drop Your Post!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
import streamlit as st
import random
songs = {
    'ballad': ['odoriko', 'labyrinth','cause you have to by lany'] ,
    'kpop' : ['tempy by exo', 'song E','song F'],
    'hiphop': ['song G', 'song H','song I'],
    'pop-punk': ['not ok by 5sos', 'no choice by fly by midnight', 'song L']
}
genre = st.selectbox("music genre of choice", list(songs.keys()))
if genre == 'ballad':
    song = random.choice(songs["ballad"])
    st.write(f"How about choosing {'odoriko'}?")
    st.audio('songs/odoriko.mp3')
    if st.selectbox("Is it to your music taste?", ['yes', 'no'], index=0):
        if st.button('no'):
         st.write(f"How about choosing {'labyrinth by taylor swift'}?")
        st.audio('songs/labyrinth.mp3')
        st.selectbox("Is it to your music taste?", ['yes', 'no'], index=0)
        if st.button ('no'):
            song = random.choice(songs['ballad'])
            st.write(f"How about choosing {'cause you have to by lany'}?")
            st.audio('songs/causeyouhaveto.mp3')
            st.selectbox("Is it to your music taste?", ['yes', 'no'], index=0)
if genre == "kpop":
    song = random.choice(songs['kpop'])
    st.write(f"How about choosing {'tempo by exo'}?")
    st.audio('songs/tempo.mp3')
elif genre == "pop-punk":
    song = random.choice(songs['pop-punk'])
    st.write(f'How about choosing {'not ok by 5sos'}?')
    st.selectbox("Is it to your music taste?", ['yes', 'no'], index=0) 
else: 
    st.write(f'How about choosing {'no choice by fly by midnight'}?')


