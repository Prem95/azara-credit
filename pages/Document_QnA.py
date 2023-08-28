import os
import tempfile
import streamlit as st
import pinecone
from langchain.llms.openai import OpenAI
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.callbacks import get_openai_callback
import yaml

# Load the YAML file
with open('secrets.yaml', 'r') as f:
    config = yaml.safe_load(f)

st.title('GPT-4 + Document Embedding (Pinecone)')

# Get OpenAI API key, Pinecone API key and environment, and source document input
openai_api_key = st.text_input("OpenAI API Key")
pinecone_api_key = st.text_input("Pinecone API Key")
pinecone_env = 'eu-west1-gcp'
pinecone_index = 'newtesting'
source_doc = st.file_uploader(
    "Upload source document", type="pdf", label_visibility="collapsed")
query = st.text_input("What is your question?")

if st.button("Submit"):
    if not openai_api_key or not pinecone_api_key or not pinecone_env or not pinecone_index or not source_doc or not query:
        st.warning(f"Please upload the document and provide the missing fields.")
    else:
        try:
            # Save uploaded file temporarily to disk, load and split the file into pages, delete temp file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(source_doc.read())
            loader = PyPDFLoader(tmp_file.name)
            pages = loader.load_and_split()
            os.remove(tmp_file.name)

            # Generate embeddings for the pages, insert into Pinecone vector database, and expose the index in a retriever interface
            pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            vectordb = Pinecone.from_documents(pages, embeddings, index_name=pinecone_index)
            retriever = vectordb.as_retriever()

            # Initialize the OpenAI module, load and run the Retrieval Q&A chain
            llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
            qa = RetrievalQA.from_chain_type(
                llm, chain_type="stuff", retriever=retriever)

            with get_openai_callback() as cb:
                response = qa.run(query)

                total_cost = cb.total_cost
                total_tokens = cb.total_tokens

                st.dataframe({
                    "Total Cost ($)": total_cost,
                    "Total Tokens": total_tokens,
                })

            st.success(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
