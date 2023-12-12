import requests
import streamlit as st
from PIL import Image
import pyperclip
import time


def send_image_and_prompt(image, prompt):
    """
    Sends an image and additional prompt to the server API.

    Args:
        image_path: Path to the image file.
        prompt: Additional text prompt.

    Returns:
        The response from the server API.
    """

    # Prepare the request
    url = "https://generative-image-caption.vercel.app/analyze"
    files = {"image": image}
    data = {"prompt": prompt}

    # Send the request
    response = requests.post(url, files=files, data=data)

    # Check for errors
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    # Return the response
    return response.json()


def main():
    st.title("Image Processing App")

    # Allow user to upload image
    uploaded_file = st.file_uploader("Choose an image:", type=["png", "jpg", "jpeg"])

    # Show prompt field only if image is uploaded
    if uploaded_file:
        prompt = st.text_input("Enter additional prompt (optional):")
        
        if st.button("Generate Caption"):
                
            # Disable button and display spinner while processing
            with st.spinner("Generating caption..."):
                response = send_image_and_prompt(uploaded_file, prompt)

            # Display the response
            if "error" in response:
                #st.error(response["error"])
                st.error("ERROR GENERATING CAPTION")
            else:
                # Split the response into individual captions
                st.caption("Please wait 1 minute before generating another caption.")
                captions = response["response"].splitlines()

                # Display each caption as a separate entity
                for caption in captions:
                    display = caption
                    print(display)
                    st.write(display)
                    # Add a copy caption
                    #st.code(display, language="python")

    else:
        st.info("Please upload an image to begin.")


if __name__ == "__main__":
    main()