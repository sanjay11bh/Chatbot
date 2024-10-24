import requests
import streamlit as st

# Function to get essay response from Ollama API
def get_ollama_response(input_text):
    try:
        response = requests.post("http://localhost:8000/essay/invoke",
                                 json={'input': {'topic': input_text}})
        response.raise_for_status()  # Check for request errors
        return response.json().get('output', {}).get('content', 'No content found')
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Function to get poem response from Ollama API
def get_ollama1_response(input_text):
    try:
        response = requests.post("http://localhost:8000/poem/invoke",
                                 json={'input': {'topic': input_text}})
        response.raise_for_status()  # Check for request errors
        return response.json().get('output', 'No content found')
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Streamlit app
st.title("LangChain Demo with Llama2 API")

# Input fields for essay and poem
input_text = st.text_input("Write an essay on")
input_text1 = st.text_input("Write a poem on")

# Process essay input
if input_text:
    essay_result = get_ollama_response(input_text)
    st.write("Essay Result:")
    st.write(essay_result)

# Process poem input
if input_text1:
    poem_result = get_ollama1_response(input_text1)
    st.write("Poem Result:")
    st.write(poem_result)
