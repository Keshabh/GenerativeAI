#Groq infering engine: A superfast computer system built to run AI models and generate answers instantly.
#Instead of using regular computer chips, it uses LPU(language processing unit)
#LPU is custom designed chip to deal especially with AI models and process them faster and effeciently.
#so less waiting time, and thats why GPT's are getting faster and faster, with their responses.

import streamlit as st
import os
from langchain_community.document_loaders import WebBaseLoader
# from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.agents import create_agent
import time
from langchain_community.embeddings import SentenceTransformerEmbeddings


from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ['API_KEY']
model_name = "intfloat/e5-small" 
#first time it runs, vector is not present, then creates all the following configurations
#for the session in a dictionary, and then uses it further for every conversation.
#for every new session, it creates new session, and for each conversation it does not have to if the session is active.
if "vector" not in st.session_state:
    st.session_state.embeddings= SentenceTransformerEmbeddings(model_name=model_name)
    st.session_state.loader= WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs=st.session_state.loader.load()
    st.session_state.chunk_documents=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    st.session_state.final_docs = st.session_state.chunk_documents.split_documents(st.session_state.docs)
    st.session_state.vectors = FAISS.from_documents(st.session_state.final_docs,st.session_state.embeddings)

st.title("ChatGroq Demo")
llm = ChatGroq(groq_api_key = GROQ_API_KEY, model="qwen/qwen3-32b")

from langchain_core.tools import StructuredTool

def retriever_fn(query: str) -> str:
    """Fetch relevant docs using your retriever and return concise text."""
    docs = st.session_state.vectors.get_relevant_documents(query)
    if not docs:
        return "No relevant documents found."
    return "\n\n".join([doc.page_content for doc in docs[:3]])

retriever_tool = StructuredTool.from_function(
    func=retriever_fn,
    name="langsmith_search",
    description="Search for relevant information about LangSmith."
)



tools= [retriever_tool]

graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant."
)

prompt = st.text_input("Input your prompt here: ")
if prompt:
    start = time.process_time()
    inputs = {"messages": [{"role": "user", "content": prompt}]}
    for chunk in graph.stream(inputs, stream_mode="updates"):
        st.write(chunk)
    st.write("Response Time: ", time.process_time() - start)



