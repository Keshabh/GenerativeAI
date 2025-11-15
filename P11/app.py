#Here will be making a streamlit application where we will be uploading multiple pdf files 
#then we will break it into chunks , apply embeddings to it, and store it in FAISS db.
#take user input, query in the db, pass the reponse from db as a prompt to LLM
#pass prompt, input i.e user query in the LLM application to return the response in a better way
from pydantic.v1 import BaseModel, ConfigDict
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import StructuredTool
import tempfile
import os
import streamlit as st
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


if "vector_store" not in st.session_state:
    st.session_state.vector_store = None


prompt = ChatPromptTemplate.from_template("""With the help of context, frame the answer with respect to the usser query, in a east to understand language.
<context>{context}</context>
Question:{input}""")

# llm = genai.GenerativeModel("gemini-2.5-pro")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)


st.subheader("AI Powered Smart PDF Reader")

with st.sidebar:
    st.header("📂 Upload PDFs")
    uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True
        )
    submit = st.button("Process!", key = "process")

pdfs = []
if uploaded_files:
    for file in uploaded_files:
        pdfs.append(file)


input = st.text_input("Ask anything related to the files uploaded..")
answerButton = st.button("Get Answer", key = "getAnswer")

flag_processed = False

def processPdf(pdfs):
        docs = []
        for pdf in pdfs:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf.read())
                tmp_file_path = tmp_file.name

            # Load using the temporary file path
            data = PyPDFLoader(tmp_file_path).load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap = 200)
            doc = splitter.split_documents(data)
            docs+=doc
        #using embedded to convert these docs it into vectors.
        st.session_state.vector_store = FAISS.from_documents(docs, embedding = embeddings)
        flag_processed = True
        st.write(flag_processed,"Files Processed Successfully !")
        return st.session_state.vector_store

if pdfs and submit:
    st.session_state.vector_store = processPdf(pdfs)

def retrieve_context(query: str):
    docs = st.session_state.vector_store.similarity_search(query, k=2)
    context = "\n\n".join(doc.page_content for doc in docs)
    return context



if answerButton and input:
    st.write("Response: ")
    context = retrieve_context(input)
    st.write(context)
    response = llm.invoke(prompt.format(context=context, input=input))
    st.write(response.content)
    
    






    




