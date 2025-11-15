#Here we will be making an invoice reader LLM application, where we will be uploading invoice image in the application
#and we can have any query regaridng the invoice, which will be answered by LLM
#additionaly prompt will be given in the code, inorder for LLM to understand what kind of tasks it is always supposed to do.
#what does image actually mean, how to answer the user query in a better way using the prompt.

from dotenv import load_dotenv
from PIL import Image
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel("gemini-2.5-pro")

st.header("Invoice Reader")
input=st.text_input("Enter query regarding the invoice submitted... ",key="input")
prompt = "You are expert in understanding the invoice image generated, where user might have queries regarding the invoice, and you will be answering the user based on question aksed using the invoice image given to you."

#upload image files
def upload_image():
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Open image with PIL
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True, width = 'stretch')
        return image
    else:
        return None

def get_gemini_response(input, prompt, image):
    response = model.generate_content([prompt,input,image])
    return response.text


image = upload_image() 
if image:
    st.write("Image submitted successfully !")

if input and image:
    response = get_gemini_response(input,prompt , image)
    st.write(response)





