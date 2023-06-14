import openai
import streamlit as st

st.set_page_config(page_title="AI Musical Composer", page_icon=":musical_note:")

openai.api_key = st.secrets["openai_secret_key"]

# Generate empty list for generated musical compositions
if 'generated_music' not in st.session_state:
    st.session_state['generated_music'] = []

# Layout of input/response containers
response_container = st.container()
input_container = st.container()


# User input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Clear input text
def clear_text():
    st.session_state["input"] = ""


with input_container:
    user_input = get_text()
    st.button("Clear Text", on_click=clear_text)


def generate_music_composition(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the Davinci model for musical composition
        prompt=user_input,
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()


with response_container:
    if user_input:
        music_composition = generate_music_composition(user_input)
        st.session_state.generated_music.append(music_composition)

    if st.session_state.generated_music:
        for i, composition in enumerate(st.session_state.generated_music):
            st.markdown(f"### Composition {i+1}")
            st.code(composition, language='text')
