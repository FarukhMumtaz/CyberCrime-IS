"""
Cybercrime Assistant - AI Chatbot Component
Direct API Implementation with Stable Models.
"""

import streamlit as st
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def render_chatbot():
    """Renders a chat interface using direct REST calls to Groq."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about cyber laws or reporting..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                api_key = os.getenv("GROQ_API_KEY")
                if not api_key:
                    st.error("API Key missing.")
                    return

                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                system_prompt = "You are a professional Cybercrime Assistant for the Pakistan NCIA. Provide guidance on PECA 2016."
                
                # Using the latest stable models
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    "temperature": 0.5
                }
                
                response = requests.post(url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    msg = response.json()["choices"][0]["message"]["content"]
                    st.markdown(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                else:
                    # Robust Fallback to 3.1 8B (Current stable lightweight model)
                    payload["model"] = "llama-3.1-8b-instant"
                    response = requests.post(url, headers=headers, json=payload, timeout=15)
                    if response.status_code == 200:
                        msg = response.json()["choices"][0]["message"]["content"]
                        st.markdown(msg)
                        st.session_state.messages.append({"role": "assistant", "content": msg})
                    else:
                        st.error(f"Chatbot Error: {response.text}")
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
