# Local LLM Project

# Imports
import streamlit as st
import ollama
import os
from pathlib import Path
from PyPDF2 import PdfReader

# Set the page configuration
st.set_page_config(page_title="Local LLM Project", layout="wide", page_icon="🤖")

st.title("🤖 Local LLM Chatbot")
st.caption("Running locally with Llama 3.2 - no data leaves this machine!")

# Initialize session state for uploaded files
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "file_contents" not in st.session_state:
    st.session_state.file_contents = {}

# File upload section in sidebar
with st.sidebar:
    st.header("📁 File Upload")
    uploaded_files = st.file_uploader(
        "Upload documents for context",
        type=["txt", "pdf", "md"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.file_contents:
                # Read file content based on file type
                try:
                    if uploaded_file.name.endswith('.pdf'):
                        # Extract text from PDF
                        pdf_reader = PdfReader(uploaded_file)
                        content = ""
                        for page in pdf_reader.pages:
                            content += page.extract_text()
                    else:
                        # Read text/markdown files
                        content = uploaded_file.read().decode("utf-8", errors="ignore")
                    
                    st.session_state.file_contents[uploaded_file.name] = content
                    st.success(f"✓ Loaded: {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error loading {uploaded_file.name}: {e}")
    
    # Display loaded files
    if st.session_state.file_contents:
        st.subheader("Loaded Documents")
        for filename in st.session_state.file_contents.keys():
            col1, col2 = st.columns([3, 1])
            col1.write(f"📄 {filename}")
            if col2.button("Remove", key=f"remove_{filename}"):
                del st.session_state.file_contents[filename]
                st.rerun()

# LLMs do not remember previous interactions by default, so we need to store the conversation history

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]
    # session_state stores information between refreshes, Without it, the chatbot would forget previous messages on every interaction !

# Display the conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message(message["role"]).write(message["content"])
    else:
        st.chat_message(message["role"]).write(message["content"])

# Function to retrieve relevant context from uploaded files
def retrieve_context(query, max_chars=2000):
    """Enhanced context retrieval with multi-document search and relevance scoring"""
    if not st.session_state.file_contents:
        return ""
    
    query_words = query.lower().split()
    results = []
    
    for filename, content in st.session_state.file_contents.items():
        # Calculate relevance score based on keyword matches
        matches = sum(1 for word in query_words if word in content.lower())
        
        if matches > 0:
            results.append({
                "filename": filename,
                "content": content[:max_chars],
                "score": matches
            })
    
    # Sort by relevance score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Build context from all relevant documents
    context = ""
    for result in results:
        context += f"\n[From {result['filename']} - Relevance: {result['score']}]:\n{result['content']}\n"
    
    return context if context else ""

# The Interaction Loop
# We collect the user's input, show it, and then get a response from Ollama LLM

if prompt := st.chat_input("What is on your mind?"):
    # 1. Display user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Placeholder for the AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # Retrieve relevant context from uploaded files
        context = retrieve_context(prompt)
        
        # Build the messages list with context
        messages = [{'role': 'user', 'content': prompt}]
        if context:
            system_message = f"You have access to the following documents:\n{context}\nUse this information to answer the user's question."
            messages.insert(0, {'role': 'system', 'content': system_message})

        # 3. Call the Local Model
        # We use 'stream=True' so the text types out like in ChatGPT
        stream = ollama.chat(
            model='llama3.2',
            messages=messages,
            stream=True,
        )

        # 4. Process the stream
        for chunk in stream:
            if chunk['message']['content']:
                content = chunk['message']['content']
                full_response += content
                response_placeholder.markdown(full_response + "▌")
        
        # Final update to remove the cursor
        response_placeholder.markdown(full_response)
    
    # 5. Save the AI's response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})