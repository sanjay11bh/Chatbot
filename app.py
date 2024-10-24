from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromtTemplate 
from langchain_core.outPut_parsers import StrOutputParser
from langchain_community.llms import Ollama

import streamlit as st 
import os
from dotenv import load_dotenv

load_dotenv()

#
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANCHAIN_API_KEY"] =os.getenv("LANGCHAIN_API_KEY")

##promt templates 

promt = ChatPromtTemplate.from_massage([
    ("System" , "You are a helpful assistant"), 
    ("user" , "Question:{question}")
])

#streamlit framework 

st.title("Langchain with Ollama")
input_text = st.text_input("Search the topic you want")

#open Ai ml call 

llm = ChatOpenAI(model = "gpt-3.5-turbo")
output_parser = StrOutputParser()

#chain  - itraction of all 

chain = promt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))


