import streamlit as st
import g4f

# Custom CSS for styling
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        color: #4F8BF9;
        background-color: #F0F2F6;
    }
    .stButton>button {
        color: white;
        background-color: #4F8BF9;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3a6bb7;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 70%;
    }
    .user-message {
        background-color: #4F8BF9;
        color: white;
        margin-left: auto;
    }
    .bot-message {
        background-color: #F0F2F6;
        color: black;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get bot response using g4f
def get_bot_response(user_input, model):
    response = g4f.ChatCompletion.create(
        model=model,
        provider=g4f.Provider.Blackbox,
        messages=[{"role": "user", "content": user_input}],
    )
    return response

# Streamlit app layout
st.title("Chatbot with Streamlit and g4f")

# Model selection dropdown
model = st.selectbox(
    "Select Model",
    options=["o3-mini", "o1", "gemini-1.5-pro", "claude-3.7-sonnet"],
    index=0,  # Default selection
)

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">{message["content"]}</div>', unsafe_allow_html=True)

# User input
user_input = st.text_input("You: ", "")

# Send button
if st.button("Send"):
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        bot_response = get_bot_response(user_input, model)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Rerun the app to update the chat display
        st.experimental_rerun()
