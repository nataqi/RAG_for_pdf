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
                response = requests.post(f"{API_URL}/api/upload", files=files)
                result = response.json() 
                if response.status_code == 200:
                    result = response.json()
                    if result['success']:
                        st.success("Document processed successfully!")
                        st.info(f"""
                            **Filename:** {result['filename']}
                            **Chunks created:** {result['chunks_count']}
                            **Total characters:** {result['total_chars']:,}
                            """)
                    else:
                        st.error(f"Error: {result.get('error', 'Unknown error')}")
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Exception occurred: {str(e)}")
            
    st.divider()
    st.subheader("📊 Database Stats")   
    
    if st.button("Refresh Stats"):
        try:
            response = requests.get(f"{API_URL}/api/stats")
            if response.status_code == 200:
                stats = response.json()
                st.metric("Total Chunks", stats['total_chunks'])
        except Exception as e:
            st.error(f"Error fetching stats: {str(e)}")
            
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    st.header("Ask Questions")
    st.info("Enter your question below to get answers based on the uploaded documents.")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("View Sources"):
                    for i, source in enumerate(message["sources"]):
                        st.markdown(f"""
                        **Source {i+1}:** {source['filename']} (Chunk {source['chunk_index']})
                        **Relevance:** {source['relevance_score']:.2%}
                        **Text:** {source['chunk_text']}
                       """)
                        st.divider()
    #chat input
    if question := st.chat_input("Type your question here..."):
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        #display user question
        with st.chat_message("user"):
            st.markdown(question)

        # Get answer from API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/ask",
                        json={"question": question, "n_results": 5}
                    )

                    if response.status_code == 200:
                        result = response.json()

                        if result['success']:
                            answer = result['answer']
                            sources = result['sources']

                            # Display answer
                            st.markdown(answer)

                            # Display sources
                            with st.expander("📄 View Sources"):
                                for i, source in enumerate(sources):
                                    st.markdown(f"""
                                    **Source {i+1}:** {source['filename']} (Chunk {source['chunk_index']})
                                    **Relevance:** {source['relevance_score']:.2%}
                                    **Text:** {source['chunk_text']}
                                    """)
                                    st.divider()

                            # Add to chat history
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer,
                                "sources": sources
                            })
                        else:
                            error_msg = f"Error: {result.get('error', 'Unknown error')}"
                            st.error(error_msg)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": error_msg
                            })
                    else:
                        st.error(f"API Error: {response.status_code}")

                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
    # Clear conversation button
    if st.sidebar.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()