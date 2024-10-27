import requests
import streamlit as st
from transformers import pipeline

# Owner name: FLAME
huggingface_api_key = "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"  # Replace with your actual Hugging Face API key
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"  # Replace with the specific LLaMA 3 model ID

# Initialize the Hugging Face pipeline
generator = pipeline("text-generation", model=model_id, use_auth_token=huggingface_api_key)

st.title("Flame's Chat App")

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages in chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Enter your question")

if prompt:
    # Display user's message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare to generate a response with the LLaMA 3 model
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Generate response using the Hugging Face pipeline
            response = generator(prompt, max_new_tokens=100)[0]["generated_text"]
            full_response = response

        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "An error occurred while fetching the response."

        # Display assistant's message
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
