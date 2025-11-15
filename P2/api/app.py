#pip install -r requirements.txt
#this command is used to install all the required libraries mentioned in requirements.txt file

#Here basically we will be first creating an API, and then using that API in another file to build a streamlit app
#In API, we will be using multiple routes , where each route will be using different LLM models to respond to user queries
#Ex: if user queries for poem, we use one model, if user queries for essay, we use another model e.t.c

from fastapi import FastAPI #to create webapis in python using fastapi framework
import uvicorn #a server to run the fastapi app 
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes #to add routes i.e url endpoints to fastapi app easily using langserve

# Create FastAPI app
app = FastAPI(
    title="LangServe Essay & Poem API",
    description="API with two endpoints: one generates essays, another generates poems.",
    version="1.0.0",
)

# Load two different models
essay_model = Ollama(model="gemma3:4b", temperature=0.7)
poem_model = Ollama(model="llama3:8b", temperature=0.7)            

#prompt template
essay_prompt = ChatPromptTemplate.from_template("Write me an essay about {topic} in just 30 words.")
poem_prompt = ChatPromptTemplate.from_template("Write me a poem about {topic} in just 3 lines.")

#essay chain
essay_chain = essay_prompt | essay_model | StrOutputParser()

#essay route
add_routes(
    app,
    essay_chain,
    path="/essay",   # Endpoint for essay generation
)

#poem chain
poem_chain = poem_prompt | poem_model | StrOutputParser()

#poem route
add_routes(
    app,
    poem_chain,
    path="/poem",    # Endpoint for poem generation
)



# Run using: uvicorn app:app --reload  
#This command is used to run the fastapi app defined in app.py file
#--reload makes sure that any changes made to the code are reflected without restarting the server
#You can access the API documentation at: http://localhost:8000/docs

# Example usage:
# To generate an essay, send a POST request to http://localhost:8000/essay with JSON body: {"input": "Your essay topic here"}
# To generate a poem, send a POST request to http://localhost:8000/poem with JSON body: {"input": "Your poem topic here"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

