from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Initialize the FastAPI app
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

# Define a ChatPromptTemplate
prompt1 = ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words.")
prompt2 = ChatPromptTemplate.from_template("Write me a poem about {topic}.")

# Instantiate the models
chat_model = ChatOpenAI()  # OpenAI LLM
llm = OllamaLLM(model="llama2")  # Ollama LLM

# Create RunnableSequence by chaining prompt and model using `|`
essay_runnable = prompt1 | chat_model
poem_runnable = prompt2 | llm

# Add routes using the RunnableSequence instances
add_routes(
    app,
    essay_runnable,  # Pass the RunnableSequence for essays
    path="/essay"
)

add_routes(
    app,
    poem_runnable,  # Pass the RunnableSequence for poems
    path="/poem"
)

# Run the FastAPI server using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
