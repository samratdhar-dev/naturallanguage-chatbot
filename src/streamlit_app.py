import streamlit as st
import plotly.io as pio
import requests
from pathlib import Path
import json

logo_path = Path(__file__).parent.parent / "docs" / "maersk.jpeg"

# Configure Streamlit page
st.set_page_config(
    page_title="AMS-SAP Analytics Chatbot",
    layout="centered"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Logo in upper left corner
logo_container = st.container()
with logo_container:
    col1, col2 = st.columns([1,3])
    with col1:
        if logo_path.exists():
            st.image(str(logo_path), width=160)
        else:
            st.write("[Logo missing]")

# API Configuration
API_BASE_URL = "http://localhost:8000"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"

def send_chat_request(question):
    """Send chat request to the API"""
    try:
        payload = {"question": question}
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=300)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"API Error: {response.status_code}"
            
    except Exception as e:
        return None, f"Error: {str(e)}"

# Header
st.title("AMS-SAP Analytics Chatbot")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
                if "fig" in message and message["fig"]:
                    try:
                        fig_from_json = pio.from_json(message["fig"])
                        st.plotly_chart(fig_from_json, use_container_width=True)
                    except:
                        st.info("Chart data received but couldn't be displayed")

# Chat input at the bottom
if prompt := st.chat_input("Ask your question about APMT analytics..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response_data, error = send_chat_request(prompt)
        
        if error:
            error_message = f"Error: {error}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
        else:
            answer = response_data.get("answer", "No response")
            st.write(answer)
            
            # Store response in session state
            message_data = {"role": "assistant", "content": answer}
            
            # Handle chart if present
            if response_data.get("fig"):
                message_data["fig"] = json.dumps(response_data["fig"])
                try:
                    fig_from_json = pio.from_json(message_data["fig"])
                    st.plotly_chart(fig_from_json, use_container_width=True)
                except:
                    st.info("Chart data received but couldn't be displayed")
            
            st.session_state.messages.append(message_data)

# Add a clear chat button in the sidebar
with st.sidebar:
    st.subheader("Chat Controls")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.write(f"**Messages in conversation:** {len(st.session_state.messages)}")
