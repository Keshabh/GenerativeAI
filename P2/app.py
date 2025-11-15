#create apis using fastAPI
from fastapi import FastAPI

#using langserve we can add routes and can have different handling for each route
from langserve import add_routes

#to use ollama llm present in local
from langchain_ollama import OllamaLLM

# Create FastAPI app
app = FastAPI(
    title="LangServe Essay & Poem API",
    description="API with two endpoints: one generates essays, another generates poems.",
    version="1.0.0",
)

# Load two different models
essay_model = OllamaLLM(model="gemma3:4b")   # Example model for essay generation
poem_model = OllamaLLM(model="llama3:8b")    # Example model for poem generation

# Add routes
add_routes(
    app,
    essay_model,
    path="/essay",   # Endpoint for essay generation
)

add_routes(
    app,
    poem_model,
    path="/poem",    # Endpoint for poem generation
)

# Run using: uvicorn app:app --reload
