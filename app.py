import requests
import streamlit as st

# Owner name: FLAME
huggingface_api_key = "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"  # Replace with your actual Hugging Face API key
url = "https://api-inference.huggingface.co/models/gpt2"  # Replace 'gpt2' with any other Hugging Face model name

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

    # Prepare to send the message to Hugging Face API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        headers = {
            'Authorization': f'Bearer {huggingface_api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 100  # Adjust max tokens as needed
            }
        }

        try:
            # Send the request to Hugging Face API
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()

            # Extract the generated response
            full_response = response_data[0].get('generated_text', '')

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            full_response = "An error occurred while fetching the response."

        # Display assistant's message
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
