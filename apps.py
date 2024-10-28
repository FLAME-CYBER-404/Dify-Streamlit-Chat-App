import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🦙💬 Flame AI Chatbot")

# Sidebar for credentials and model settings
with st.sidebar:
    st.title('🦙💬 Flame AI Chatbot')
    st.write('This chatbot is created using the open-source Llama 2 LLM model from Meta.')
    
    # Replicate API token input
    replicate_api = st.text_input('Enter Replicate API token:', type='password')
    if not replicate_api:
        st.warning('Please enter your API key to proceed.', icon='⚠️')
    else:
        st.success('API key loaded successfully!', icon='✅')
    
    # Set environment variable for API key
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    
    # Model and parameters selection
    st.subheader('Models and Parameters')
    selected_model = st.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'])
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    else:
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    
    # Additional model settings
    temperature = st.slider('Temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=20, max_value=80, value=50, step=5)
    
    st.write("Owner • Flame")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function to generate response using LLaMA 2 model via Replicate
def generate_llama2_response(prompt_input):
    conversation_history = "You are a helpful assistant. Respond as 'Assistant' only."
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_history += f"\n\n{role}: {msg['content']}"
    
    output = replicate.run(
        llm,
        input={
            "prompt": f"{conversation_history}\n\nUser: {prompt_input}\nAssistant: ",
            "temperature": temperature,
            "top_p": top_p,
            "max_length": max_length,
            "repetition_penalty": 1
        }
    )
    return output

# Accept user input for the chatbot
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate and display assistant's response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''.join(response)
            placeholder.markdown(full_response)
    
    # Append assistant's response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
