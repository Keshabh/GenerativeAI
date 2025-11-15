import streamlit as st
import requests #to make API calls to the FastAPI server

def get_essay_api_response(input_text1):
    response = requests.post(
        "http://localhost:8000/essay/invoke",
        json={"input": {'topic': input_text1}})
    return response.json().get("output", "No response")

def get_poem_api_response(input_text2):
    response = requests.post(
        "http://localhost:8000/poem/invoke",
        json={"input": {'topic': input_text2}})
    return response.json().get("output", "No response")
    

st.title("LangServe Essay & Poem API Client")
input_text1 = st.text_input("Enter a topic for Essay generation:")
input_text2 = st.text_input("Enter a topic for Poem generation:")


if input_text1:
        st.write(get_essay_api_response(input_text1))

if input_text2:
        st.write(get_poem_api_response(input_text2))
