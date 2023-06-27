import openai
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from PIL import Image

# Set OpenAI API key
openai.api_key = st.secrets["openai_secret_key"]

# Page configuration
st.set_page_config(page_title="LinguaBot")

# Sidebar contents
with st.sidebar:
    image_path = "linguabot.png"  # Path to the Linguabot image
    image = Image.open(image_path)
    st.image(image)
    st.markdown("# About")
    st.markdown(
        """
        <p style='text-align: justify;'> 
        I am LinguaBot, your language translation assistant. With my expertise in multilingual communication, I can help you break through language barriers. Whether you need to translate a phrase, understand foreign text, or communicate effectively in another language, I'm here to assist you. Let's bridge the gap between languages and enable seamless global communication together.
        """,
        unsafe_allow_html=True,
    )


# Language selection
languages = [
    ("English", "en"),
    ("Arabic", "ar"),
    ("Chinese", "zh-CN"),
    ("Dutch", "nl"),
    ("Finnish", "fi"),
    ("Filipino", "tl"),
    ("French", "fr"),
    ("German", "de"),
    ("Greek", "el"),
    ("Hindi", "hi"),
    ("Hungarian", "hu"),
    ("Italian", "it"),
    ("Japanese", "ja"),
    ("Korean", "ko"),
    ("Nepali", "ne"),
    ("Polish", "pl"),
    ("Portuguese", "pt"),
    ("Romanian", "ro"),
    ("Russian", "ru"),
    ("Spanish", "es"),
    ("Swedish", "sv"),
    ("Thai", "th"),
    ("Turkish", "tr"),
    ("Vietnamese", "vi")
]


source_language = st.selectbox("Source Language", [lang[0] for lang in languages])
target_language = st.selectbox("Target Language", [lang[0] for lang in languages])

# User input
with st.container():
    user_input = st.text_input("You: ", "")

    if st.button("Speak"):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            st.write("Listening...")
            audio = recognizer.listen(source)

        try:
            st.write("Processing...")
            user_input = recognizer.recognize_google(audio)
            st.text_area("You:", value=user_input, height=100)
        except sr.UnknownValueError:
            st.write("Could not understand audio.")
        except sr.RequestError as e:
            st.write("Error: {0}".format(e))

# Translation
if user_input:
    messages = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": "Translate the text from {} to {} without pronunciation.".format(source_language, target_language)}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3
    )
    translation = response.choices[0].message.content.split('(', 1)[0].strip()

    st.text_area("Translation:", value=translation, height=150)

    # Text-to-speech conversion
    target_lang_code = next((lang[1] for lang in languages if lang[0] == target_language), None)
    tts = gTTS(text=translation, lang=target_lang_code, slow=False)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")

    os.unlink(temp_file.name)  # Remove the temporary file after playing

