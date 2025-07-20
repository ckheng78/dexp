import streamlit as st
import random
import time
import requests

chat_api_url = "http://127.0.0.1:8000/ask"  # Update with your actual chat API URL

def run():
    st.title("Logistics Data Explorer")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Please pose a question?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            # Show thinking indicator
            with st.spinner("Agent is thinking..."):
                try:
                    # Make API request with proper parameter name
                    response = requests.get(f'{chat_api_url}?prompt={prompt}', timeout=60)
                    if response.status_code == 200:
                        full_response = response.json().get("response", "No response from server.")
                    else:
                        full_response = f"Error: Server returned status {response.status_code}"
                except requests.exceptions.Timeout:
                    full_response = "Error: Request timed out. Please try again."
                except requests.exceptions.RequestException as e:
                    full_response = f"Error: Unable to connect to server. {str(e)}"
           
            # Display the final response
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    run()