#OPEN SOURCE (present in local, does not require API KEY)

#streamlit import is to make a web app interface for chatbot
import streamlit as st
import os
#this gives a proper template of comversation between ai and user.
from langchain.prompts import ChatPromptTemplate

import requests

from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")

#this is a json api call with API key, which takes the text and fetches the prompt
def ask_openrouter(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-3.5-turbo",  # or try "openai/gpt-4o"
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{input}")
])

# Streamlit UI
st.set_page_config(page_title="Open Router Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 GPT3:5 TURBO Chatbot (Open Router AI Web LLM)")

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt_text := st.chat_input("Type your message..."):
    # Add user message to history(what ever text has been typed and take it to conversaiton area in the page)
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    response = ask_openrouter(prompt_text)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
