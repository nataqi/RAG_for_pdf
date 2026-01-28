import streamlit as st
import os
import requests
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")


st.set_page_config(page_title="Document Q&A Assistant", page_icon=":books:", layout="wide")
st.title("📚 Document Q&A Assistant")
st.markdown("Upload PDF documents and ask questions about their content using RAG")

doc_upload = st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF file",
    type=['pdf'],
    help="Upload a PDF document to analyze"
)

if uploaded_file is not None:
    st.info(f"Selected file: **{uploaded_file.name}** ({uploaded_file.size} bytes)")
    
    if st.button("Process Document", type = "primary"):
        with st.spinner("Processing document..."):
            try:
                files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
                response = requests.post(f"{API_URL}/upload", files=files)
                result = response.json() 
                if response.status_code == 200:
                    result = response.json()
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Exception occurred: {str(e)}")
            
                
    
    
