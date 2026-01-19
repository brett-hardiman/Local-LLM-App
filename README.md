Local LLM Chat App

A simple chat-based local Large Language Model (LLM) application built in Python using Ollama and Streamlit — running fully on your machine with no cloud APIs or external servers. Your data stays private, and there are no API fees.

🚀 Overview

This project demonstrates how to:

 - Run an LLM locally using Ollama

 - Build a client UI with Streamlit

 - Maintain chat history in a conversational interface

It’s a great learning project to understand how local LLM inference works, and can be expanded for privacy-first AI use cases.


🧠 Features

 - Local execution — everything runs on your computer

 - Python-based UI using Streamlit

 - Responsive chat interface with streaming output

 - Conversation memory with Streamlit’s session state

 - Works with Llama 3.2 (or other models) via Ollama


📦 Prerequisites

Before getting started, make sure you have:

 - Python 3.8+ installed

 - Ollama installed and initialized on your system

 - At least 8–16GB of RAM (recommended for best performance)
   

💡 How It Works

- Streamlit UI — Displays a friendly chat interface.

 - Session State — Maintains conversation history.

 - Ollama Chat — Calls the local model with streaming responses.

 - Typing Effect — Uses stream=True for progressive output.

 
 📖 Resources

 - Ollama — Local model management tool

 - Streamlit — Python UI framework

 - Llama 3.2 — Example LLM used in this project
   

🙏 Credits & Acknowledgments

This project was inspired by and built following the guide:

“Building Your First Local LLM App”
Author: Aman XAI
Website: https://amanxai.com

The article provides a clear, beginner-friendly walkthrough for running a local LLM using Ollama and Streamlit, and served as the foundational reference for this project’s structure and implementation. I took it a step further by adding in multi-document search, file upload, and context retrieval!
