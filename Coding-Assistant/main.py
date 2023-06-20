import openai
import streamlit as st
from PIL import Image
import os
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="CodePal", page_icon=":computer:")

openai.api_key = st.secrets["openai_secret_key"]
# # And the root-level secrets are also accessible as environment variables:
# os.environ["openai_secret_key"] == st.secrets["openai_secret_key"]

page_bg = f"""
<style>
[data-testid="stSidebar"] {{
background-color:#D3D3D3;

}}

[data-testid="stToolbar"] {{
background-color:#FCFCFC;

}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar contents
with st.sidebar:
    image_path = os.path.join(os.path.dirname(__file__), 'codepal.png')
    image = Image.open(image_path)
    st.image(image)
    st.markdown("<h1 style='text-align: left;> About </h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: justify;'> 
        Welcome to CodePal, your reliable companion for all your coding adventures! As a trusted assistant, CodePal is here to guide you through the intricacies of programming and help you conquer any coding challenges you may face. With its vast knowledge of programming languages, algorithms, and best practices, CodePal will be by your side, offering practical insights, solutions, and personalized suggestions to enhance your coding skills. Whether you're a beginner or an experienced coder, let CodePal be your go-to partner in your coding journey!""",
        unsafe_allow_html=True,
    )


# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ['Hello, I am CodePal. How can I help you?']
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
    "content": "You are a coding assistant bot named CodePal, providing individuals with guidance and support in coding and programming tasks. "
    "You should use your knowledge of programming languages, algorithms, data structures, and software development best practices "
    "to assist users in solving coding problems, understanding concepts, and improving their coding skills. Only respond to queries related to coding and programming. ",
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
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        if len(st.session_state['past']) == 0:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["generated"][i], key=str(i))
        else:
            for i in range(len(st.session_state['generated'])):
                if i < len(st.session_state['past']):
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

