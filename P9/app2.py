from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-2.5-pro") 
#for the model to remember the past conversation, so each conversation is a context for any questions asked.
chat = model.start_chat(history=[])
def get_gemini_response(question):
    
    response=chat.send_message(question,stream=True)
    return response

def user_message(message):
    st.markdown(f"""
    <div style="
        background-color:#DCF8C6;
        padding:10px;
        border-radius:10px;
        margin:5px;
        max-width:70%;
        margin-left:auto;
        text-align:right;
        color:black;
    ">
        {message}
    </div>
    """, unsafe_allow_html=True)

def bot_message(message):
    st.markdown(f"""
    <div style="
        background-color:#E5E5EA;
        padding:10px;
        border-radius:10px;
        margin:5px;
        max-width:70%;
        color:black;
    ">
        {message}
    </div>
    """, unsafe_allow_html=True)


##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.title("💬 Gemini Chat")

# Initialize session state for chat history if it doesn't exist
#using session_state to remeber the conversation, inorder to display them.
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Ask Anything... ",key="input")

if  input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    if role == "You":
        user_message(text)
    if role == "Bot":
        bot_message(text)
    



    
