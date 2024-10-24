import streamlit as st
import os 

from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
import time

from langchain.embeddings import OllamaEmbeddings

from dotenv import load_dotenv
load_dotenv()

## load the GROQ and OPENAI API KEY 
##os.environ["OPENAI_API_KEY"] =os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] =os.getenv("LANGCHAIN_API_KEY")

groq_api_key = os.getenv("GROQ_API_KEY")

st.title("Chatgroq with Llama3 demo")
llm = ChatGroq(groq_api_key=groq_api_key , 
               model_name ="Llama3-8b-8192" )

prompt = ChatPromptTemplate.from_template(
"""
Answer the question based on the provided contex only .
Please provide the most accurate response based on the question
<context>
{context}
<context>
Question :{input}
"""
)

prompt1 = st.text_input("Enter the Question from Documents")

def vector_embedding():
    if "vectors"  not in st.session_state:

        # st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.embeddings = OllamaEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")  ## Data Ingestion
        st.session_state.docs = st.session_state.loader.load() ## Documents loading 
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size =1000 , chunk_overlap = 200)  ## chhunk Creation
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])  ##spliting 
        st.session_state.vector = FAISS.from_documents(st.session_state.final_documents ,st.session_state.embeddings)  ##vector OPenAI embedding


if st.button("Documents Embedding"):
    vector_embedding()
    st.write("vector store Db is Ready")


if prompt1:
    document_chain = create_stuff_documents_chain(llm , prompt)
    retriver = st.session_state.vectors.as_retriever()
    retreival_chain = create_retrieval_chain(retriver , document_chain)

    start = time.process_time()
    retreival_chain.invoke({'input':prompt1})
    print("Response time :" ,time.process_time() - start)
    st.write(response['answer'])

        #With Streamlit Expander 
    with st.expander("Document Similarity Search"):
        # Find the relevent chunks 
        for i , doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("..................")





