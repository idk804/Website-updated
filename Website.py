import streamlit as st
import g4f

# List the models to be used
models = [
    "o1", 
    "o3-mini", 
    "deepseek-r1", 
    "gpt-4o", 
    "claude-3.7-sonnet"
]

# Set up the title and layout of the page
st.set_page_config(page_title="Modern Chatbot", layout="centered")
st.title("💬 Modern Chatbot with G4F")

# Adding custom CSS to style the page
st.markdown("""
<style>
    body {
        font-family: 'Helvetica Neue', sans-serif;
        background-color: #F7F8FA;
        margin: 0;
        padding: 0;
        color: #333;
    }

    .chat-container {
        max-width: 600px;
        margin: 20px auto;
        background-color: #fff;
        border-radius: 15px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        padding: 25px;
    }

    .chat-header {
        text-align: center;
        margin-bottom: 20px;
        font-size: 28px;
        font-weight: bold;
        color: #4CAF50;
    }

    .input-container {
        margin-top: 30px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .message {
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-size: 16px;
        max-width: 80%;
        word-wrap: break-word;
        line-height: 1.4;
    }

    .user-message {
        background-color: #DCF8C6;
        margin-left: auto;
        border-radius: 15px 15px 0 15px;
    }

    .bot-message {
        background-color: #E4E6EB;
        border-radius: 15px 15px 15px 0;
    }

    .input-box {
        width: 100%;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        font-size: 16px;
        box-sizing: border-box;
        transition: border-color 0.3s ease;
    }

    .input-box:focus {
        border-color: #4CAF50;
    }

    .send-button {
        background-color: #4CAF50;
        color: white;
        padding: 14px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        font-size: 18px;
        transition: background-color 0.3s ease;
    }

    .send-button:hover {
        background-color: #45a049;
    }

    .model-select {
        font-size: 16px;
        padding: 10px;
        border-radius: 10px;
        background-color: #fff;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)

# Function to get G4F responses for selected models
def get_model_responses(model: str, prompt: str):
    try:
        # Fetch response from the current model
        response = g4f.ChatCompletion.create(
            model=model,  # specify the model
            provider=g4f.Provider.Blackbox,  # specify the provider
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Main Chatbot logic
def chat():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        if message["sender"] == "user":
            st.markdown(f'<div class="message user-message">{message["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message bot-message">{message["text"]}</div>', unsafe_allow_html=True)

    # Dropdown to select the model
    model_choice = st.selectbox("Choose a Model:", models, key="model", label_visibility="collapsed", index=0, help="Select the chatbot model")

    # User input for the chatbot
    user_input = st.text_input("Type your message:", key="input", placeholder="Ask me anything...", label_visibility="collapsed")

    if user_input:
        # Store user message
        st.session_state.chat_history.append({"sender": "user", "text": user_input})

        # Get response from selected model
        bot_response = get_model_responses(model_choice, user_input)

        # Store bot response
        st.session_state.chat_history.append({"sender": "bot", "text": bot_response})

        # Call st.rerun() to refresh the page and display updated chat
        st.rerun()

# Run the chatbot function
chat()
