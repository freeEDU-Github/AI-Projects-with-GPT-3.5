import io
import os
import streamlit as st
from PIL import Image
from bardapi import Bard

def main():
    with st.sidebar:
        image_path = os.path.join(os.path.dirname(__file__), 'visual_llm.png')
        image = Image.open(image_path)
        st.image(image, use_column_width=True)

        st.markdown("<h1 style='text-align: left;'> About </h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style='text-align: justify;'> 
            The Visual LLM is your gateway to an innovative and interactive language experience. Harnessing the cutting-edge capabilities of Google Bard, this application combines the power of state-of-the-art Language Models (LLM) with a user-friendly interface. 
            <br><br>With Visual LLM, you can effortlessly generate natural language responses, captions, or text based on the context of images and user prompts. 
            Whether you want to describe images, write creative captions, or explore a myriad of language tasks, Visual LLM is here to assist you at every step of your journey.""",
            unsafe_allow_html=True,
        )

    st.title("Visual LLM")

    # Layout containers for input and response
    input_container = st.container()
    response_container = st.container()

    # Call your functions for image processing and LLM response
    image, prompt = process_input(input_container)
    get_response(response_container, prompt, image)


def process_input(container):
    container.markdown("## Input")

    # Initialize the 'image' variable to None
    image = None

    # Provide a list of example images for users to choose from
    example_images = ["image1.jpg", "image2.jpg", "image3.jpg"]

    selected_image = container.selectbox("Select an example image or upload your own:",
                                         ["Choose an option"] + example_images)

    if selected_image == "Choose an option":
        user_uploaded_image = container.file_uploader("Upload your own image:", type=["jpg", "jpeg", "png"])

        if user_uploaded_image is not None:
            # Process the uploaded image, e.g., using PIL
            image = Image.open(user_uploaded_image)
            container.image(image, caption="Uploaded Image", use_column_width=True)

    else:
        # Load the selected sample image and display it
        image_path = os.path.join(os.path.dirname(__file__), "images", selected_image)
        image = Image.open(image_path)
        container.image(image, caption="Example Image", use_column_width=True)

    # Add a text input field for user prompt
    prompt = container.text_area("Write your prompt here:", "")
    return image, prompt


def get_response(container, prompt, image):
    container.markdown("## Response")

    if prompt:

        # token = st.secrets["BARD_API_KEY"]
        # # Initialize the Bard API client
        # bard = Bard(token=token)

        # bard = Bard(token_from_browser=True)

        bard = Bard()
        # Convert the image to bytes
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='JPEG')
        image_bytes = image_bytes.getvalue()

        # Send the prompt and image bytes to the Bard API for explanation
        response = bard.ask_about_image(prompt, image_bytes)['content']

        # Display the response
        container.write(response, unsafe_allow_html=True, style="text-align: justify;")

        # Use the bard.speech library to convert the response to speech
        st.audio(bard.speech(response))
    else:
        container.warning("Please write a prompt to get a response.")


if __name__ == "__main__":
    main()
