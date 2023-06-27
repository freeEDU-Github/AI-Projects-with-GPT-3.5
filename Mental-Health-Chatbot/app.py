import openai
import streamlit as st
from PIL import Image
import os
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Mindi Chatbot", page_icon=":robot:")

openai.api_key = st.secrets["openai_secret_key"]
# # And the root-level secrets are also accessible as environment variables:
# os.environ["openai_secret_key"] == st.secrets["openai_secret_key"]

page_bg = f"""
<style>
[data-testid="stSidebar"] {{
background-color:#2C3C2C;

}}

[data-testid="stToolbar"] {{
background-color:#FCFCFC;

}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar contents
with st.sidebar:
    image_path = os.path.join(os.path.dirname(__file__), 'mindi.png')
    image = Image.open(image_path)
    st.image(image)
    st.markdown("<h1 style='text-align: left;> About </h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: justify;'> Introducing Mindi, your compassionate companion for mental well-being! Whenever you're experiencing sadness, worry, or tension, Mindi is here to support you and assist in understanding your emotions. Feel at ease discussing your mental health worries with Mindi, as it offers a safe and comforting space. Feel free to reach out and chat with Mindi whenever you need, no matter where you are! </p>
        """,
        unsafe_allow_html=True,
    )

    add_vertical_space(2)
    option = st.selectbox(
        'Tell me where you are located:',
        (
            'Finland',
            'Sweden',
            'Germany',
            'Thailand',
            'Philippines',
            'USA',
        ),
        label_visibility="visible",
    )

    if option == 'Finland':
        word = 'Finnish'
    elif option == 'Sweden':
        word = 'Swedish'
    elif option == 'Germany':
        word = 'German'
    elif option == 'Thailand':
        word = 'Thai'
    elif option == 'Philippines':
        word = 'Tagalog'
    elif option == 'USA':
        word = 'English'

# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['Hello, I am Mindi. How may I help you?']
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Layout of input/response containers
response_container = st.container()
input_container = st.container()


# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Clear input text
def clear_text():
    st.session_state["input"] = ""


## Applying the user input box
with input_container:
    user_input = get_text()
    st.button("Clear Text", on_click=clear_text)

messages = [
    {
        "role": "system",
        "content": "You are a friendly psychologist named Mindi, providing individuals with guidance and advice on managing emotions, stress, anxiety, "
                   "and other mental health issues. You should use your knowledge of cognitive behavioral therapy, meditation techniques, "
                   "mindfulness practices, and other therapeutic methods in order to create strategies that the individual can implement "
                   "to improve their overall well-being. Only respond to queries related to mental health. "
                   "Make your responses friendly and include a word related to " + word + " with a beautiful meaning and emojis.",
    }
]


def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply


## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = CustomChatGPT(user_input)
        if len(st.session_state['past']) == 0:
            st.session_state.past.append('Location: ' + option)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        if len(st.session_state['past']) == 0:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["generated"][i], key=str(i))
        else:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))
