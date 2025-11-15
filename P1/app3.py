#A chatbot using open-source LLM OLLAMA using Langchain

#Libs Imports
from langchain_core.prompts import ChatPromptTemplate #provides structured template to chat with models
from langchain_core.output_parsers import StrOutputParser #helper class which converts models output into plain texts
import streamlit as st #to build interactive webapps using python
import os #to work with system paths, files, environment variables
from langchain_community.llms import Ollama #to connect with ollama models


#python -m venv .venv
#this command when run creates a venv environment basically creates a file named .venv.

#.venv\Scripts\activate 
#this command is used to activate the venv environment, which switches the  syetems usage of python libs to the libs defined inside venv file.

#It basically creates a private workspace environemnt independent of system.(so that there is no interference, and version controlled libs can be used as per need)

#after environment is switched, we see something like this: (.venv) C:\Users\Keshabh\project>

# if we install any libs here such as : pip install streamlit
# It is installed inside this environment , and not in the system

#prompt template
#1st line is an instruction to system to define the role of the AI assistant
#2nd line is the user input format where {input} is a placeholder for user query
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Please respond to user queries in a concise manner."),
    ("user", "Question:{input}")
])

#initialize the ollama model
#temperature = 0 means deterministic responses
#temperature = 1 or more means more creative responses
#temperature = 0.7 means balanced responses
llm = Ollama(model="gemma3:4b", temperature=0.7)
output_parser = StrOutputParser() #initialize the output parser to convert model output to plain text
chain = prompt | llm | output_parser #create a chain by combining prompt template, llm model and output parser

#streamlit web app
st.title("🤖 Gemma3:4b Chatbot with Ollama (Local LLM)")
input_text = st.text_input("Search any topic...")


if input_text:
    #invoke the chain with user input
    response = chain.invoke({"input": input_text})
    st.write(response)

    
#streamlit run app3.py
#this command is used to run the streamlit app defined in app3.py file