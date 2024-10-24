from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama


import streamlit as st 
import os
from dotenv import load_dotenv

load_dotenv()

#
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANCHAIN_API_KEY"] =os.getenv("LANGCHAIN_API_KEY")

#promt templates 

promt = ChatPromptTemplate.from_messages([
    ("system" , "You are a helpful assistant"), 
    ("user" , "Question:{question}")
])

#streamlit framework 

st.title("Langchain with Ollama")
input_text = st.text_input("Search the topic you want")

#open Ai ml call 

llm = Ollama(model = "llama2")
output_parser = StrOutputParser()

#chain  - itraction of all 

chain = promt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))