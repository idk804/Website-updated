import streamlit as st
import g4f

# Custom CSS for modern styling and animations
st.markdown("""
    <style>
    /* General styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f5f5f5;
    }
    .stTextInput>div>div>input {
        color: #4F8BF9;
        background-color: #ffffff;
        border: 1px solid #4F8BF9;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton>button {
        color: white;
        background-color: #4F8BF9;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3a6bb7;
    }
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        max-width: 70%;
        animation: fadeIn 0.5s ease;
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
    /* Password screen styling */
    .password-screen {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
    }
    .password-screen h1 {
        font-size: 2.5rem;
        color: #4F8BF9;
        margin-bottom: 20px;
    }
    .password-screen input {
        margin-bottom: 20px;
    }
    /* Animation for chatbot reveal */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# Password protection
PASSWORD = "rosana2012"  # Set your password here

# Initialize session state for chat history and password verification
if "messages" not in st.session_state:
    st.session_state.messages = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Function to get bot response using g4f
def get_bot_response(user_input, model):
    response = g4f.ChatCompletion.create(
        model=model,
        provider=g4f.Provider.Blackbox,
        messages=[{"role": "user", "content": user_input}],
    )
    return response

# Password input screen
if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="password-screen">
            <h1>Welcome to Private Chatbot</h1>
            <p>Enter the password to access the site.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    password_input = st.text_input("Password:", type="password", key="password_input")
    if st.button("Submit"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
        else:
            st.error("Incorrect password. Please try again.")

# If authenticated, show the chatbot interface
if st.session_state.authenticated:
    st.markdown(
        """
        <div style="animation: fadeIn 1s ease;">
            <h1 style="text-align: center; color: #4F8BF9;">Private Chatbot</h1>
            <p style="text-align: center; color: #666;">You are now accessing the private chatbot.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
