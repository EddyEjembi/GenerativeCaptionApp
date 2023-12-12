import requests
import streamlit as st
from PIL import Image
import threading
import time


def send_image_and_prompt(image, prompt):

    # Prepare the request
    url = "https://generative-image-caption.vercel.app/analyze"
    files = {"image": image}
    data = {"prompt": prompt}

    # Send the request
    response = requests.post(url, files=files, data=data)

    # Check for errors
    if response.status_code != 200:
        #raise Exception(f"Error: {response.status_code} - {response.text}")
        st.info(f"Error: ERROR GENERATING CAPTION... PLEASE TRY AGAIN.")

    # Return the response
    return response.json()


def main():
    st.title("Social Media Image Caption Generator")
    st.subheader("Generate exciting and engaging social media captions for your images")

    #message = []
    # Allow user to upload image
    uploaded_file = st.file_uploader("Choose an image:", type=["png", "jpg", "jpeg"])


    # Show prompt field only if image is uploaded
    if uploaded_file:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", width=300)

        prompt = st.text_input("Enter an additional prompt (optional):")

        # Get the current session state
        session_state = st.session_state

        # Display button and handle button click logic
        if "last_click_time" not in session_state:
            session_state.last_click_time = 0

        elapsed_time = time.time() - session_state.last_click_time
        
        # Generate caption button
        if st.button("Generate Caption"):
            if elapsed_time > 60:
                    
                # Disable button and display spinner while processing
                with st.spinner("Generating caption..."):
                    session_state.last_click_time = time.time()  # Update last click time
                    response = send_image_and_prompt(uploaded_file, prompt)

                    # Store the original captions in session state
                    session_state.original_captions = response.get("response", "").splitlines()

                # Display the response
                if "error" in response:
                    #st.error(response["error"])
                    st.error("ERROR GENERATING CAPTION")
                else:
                    # Split the response into individual captions
                    st.info("Please wait 1 minute before generating another caption.")
                    captions = response["response"].splitlines()
                    print(type(captions))

                    # Display each caption as a separate entity
                    for caption in captions:
                        display = caption
                        print(display)
                        st.write(display)
                        # Add a copy caption
                        #st.code(display, language="python")
                    
            else:
                st.info(f"Please wait {round(60 - elapsed_time)} seconds before generating another caption.")
                #captions = response["response"].splitlines()
                st.caption("Previous Captions:")
                original_captions = st.session_state.get("original_captions", [])
                for caption in original_captions:
                        display = caption
                        st.write(display)
    else:
        st.info("Please upload an image to begin.")


if __name__ == "__main__":
    main()