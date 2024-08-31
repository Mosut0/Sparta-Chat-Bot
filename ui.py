import streamlit as st
import requests
import json

st.set_page_config(page_title="RAG Chatbot")
st.title("SPARTA Chatbot")

# Add a file uploader at the top of the app
uploaded_file = st.file_uploader("Choose a file to add more context!")

if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

if uploaded_file is not None and uploaded_file != st.session_state.last_uploaded_file:
    # Send to endpoint
    file_content = uploaded_file.read()

    file_url = "http://127.0.0.1:8000/add_document_file"

    # Send the file to the endpoint
    response = requests.post(file_url, files={"file": (uploaded_file.name, file_content)})

    # Check the response
    if response.status_code == 200:
        st.success("File uploaded successfully")
        st.session_state.last_uploaded_file = uploaded_file
    else:
        st.error("File upload failed")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

input_text = st.chat_input("Chat with your bot here")

if input_text:
    with st.chat_message("user"):
        st.markdown(input_text)
    
    st.session_state.chat_history.append({"role":"user", "text":input_text})

    with st.spinner('Thinking...'):
        # Make the API call
        response = requests.post('http://127.0.0.1:8000/user_query', data=({'query': input_text}))
        chat_response = response.text

    with st.chat_message("assistant"):
        st.markdown(chat_response)
    
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response})
