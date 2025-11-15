from dotenv import load_dotenv
from PIL import Image
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

#fucntion to load responses from gemini  pro model
def get_gemini_response(question):
    # Stream the response as it's being generated
    response = model.generate_content(question)
    return response.text


#function to read uploaded image, and answer any question on it.
# def get_img_gemini_response(img, question):
     

st.set_page_config("Q&A Demo")
st.header("Gemini LLM Application")
input = st.text_input("Input: ", key = "input")
submit = st.button("Ask the question",key = "button1")
if submit:
        response = get_gemini_response(input)
        st.subheader("The response is: ")
        st.write(response)




def upload_image():
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Open image with PIL
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True, width = 'stretch')
        return image
    else:
        return None


st.title("Image Upload Demo")
image = upload_image()   
if image is not None:
    st.success("Image successfully uploaded!")

input2 = st.text_input("Input: ", key = "input2")
submit2 = st.button("Ask the question",key="button2")

if submit2:
    if input2:
      response = model.generate_content([input2,image])      
    else:
      response = model.generate_content(image)
    st.write(response.text)

