#OPEN SOURCE (present in local, does not require API KEY)
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

# Initialize Ollama model
llm = OllamaLLM(model="gemma3:4b")

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{input}")
])

# Streamlit UI
st.set_page_config(page_title="Gemma3 Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemma3:4b Chatbot (Local with Ollama)")

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt_text := st.chat_input("Type your message..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    # Generate response
    chain = prompt | llm
    response = chain.invoke({"input": prompt_text})

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
