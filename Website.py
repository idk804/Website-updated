import streamlit as st
from g4f.client import Client
import os

# Initialize the G4F client
client = Client(provider="g4f.Provider.Blackbox")

# Available models
available_models = [
    "o1",  # Model 1
    "o3-mini",  # Model 2
    "deepseek-r1",  # Model 3
    "gpt-4o",  # Model 4
    "claude-3.7-sonnet"  # Model 5
]

# Function to handle text or vision response
def gpt_response(prompt, selected_model, images=None):
    try:
        if images:
            # Save uploaded images to a local directory
            image_dir = "uploaded_images"
            os.makedirs(image_dir, exist_ok=True)  # Ensure the directory exists
            saved_images = []
            for image in images:
                file_path = os.path.join(image_dir, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.getbuffer())  # Save image content
                saved_images.append([open(file_path, "rb"), file_path])

            # Vision + Text response
            response = client.chat.completions.create(
                model=selected_model,
                messages=[{"role": "user", "content": prompt}],
                images=saved_images,
            )
        else:
            # Text-only response
            response = client.chat.completions.create(
                model=selected_model,
                messages=[{"role": "user", "content": prompt}],
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred with G4F API: {e}"

# Apply custom CSS for a modern UI
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f7fa;
            font-family: 'Roboto', sans-serif;
        }

        .main-container {
            max-width: 900px;
            margin: 50px auto;
            padding: 2rem;
            border-radius: 15px;
            background: white;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        .title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a73e8;
            text-align: center;
        }

        .subtitle {
            font-size: 1.1rem;
            color: #333;
            text-align: center;
            margin-bottom: 2rem;
        }

        .input-card {
            background: #e3f2fd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        textarea, select, input {
            font-size: 16px !important;
            border-radius: 8px !important;
            padding: 12px !important;
            width: 100%;
        }

        .stButton > button {
            background-color: #1a73e8;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            padding: 12px 24px;
            transition: 0.3s;
            cursor: pointer;
        }

        .stButton > button:hover {
            background-color: #1558b0;
        }

        .response-card {
            background: #f1f8e9;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            font-size: 16px;
            color: #333;
            font-weight: 500;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            white-space: pre-wrap;
        }

        .message-container {
            margin-bottom: 1.5rem;
        }

        .user-message {
            padding: 10px;
            border-radius: 8px;
            background-color: #d1e8ff;
            max-width: 80%;
            margin: 5px 0;
        }

        .bot-message {
            padding: 10px;
            border-radius: 8px;
            background-color: #f1f8e9;
            max-width: 80%;
            margin: 5px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout setup
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title and subtitle
st.markdown('<h1 class="title">🚀 Modern AI Chatbot</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Interact with AI models by sending text and images. Enjoy the chat experience!</p>',
    unsafe_allow_html=True,
)

# Input area card
st.markdown('<div class="input-card">', unsafe_allow_html=True)
prompt = st.text_area(
    "Enter your prompt:",
    placeholder="Describe something or ask about images...",
    height=150,
)
selected_model = st.selectbox(
    "Select a model:",
    options=available_models,
)

# Image upload button
uploaded_images = st.file_uploader(
    "Upload an image to send with your message:",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
)

# Chat history container
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to display messages in chat format
def display_chat_history():
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="message-container"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)
        elif message["role"] == "bot":
            st.markdown(f'<div class="message-container"><div class="bot-message">{message["content"]}</div></div>', unsafe_allow_html=True)

display_chat_history()

st.markdown('</div>', unsafe_allow_html=True)

# Button to send message
if st.button("Send Message"):
    if not prompt.strip():
        st.error("⚠️ Please provide a valid prompt!")
    else:
        # Add user's message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Generate response based on user input
        if uploaded_images:
            response = gpt_response(prompt, selected_model, uploaded_images)
        else:
            response = gpt_response(prompt, selected_model)

        # Add bot's response to chat history
        st.session_state.chat_history.append({"role": "bot", "content": response})

        # No need to call st.experimental_rerun() or any similar function
        # Streamlit will automatically rerun when session state changes

# Closing container
st.markdown('</div>', unsafe_allow_html=True)
