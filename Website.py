import streamlit as st
from g4f.client import Client

# Initialize the G4F client
client = Client()

# Updated list of available models
available_models = [
    "gpt-4o-mini",  # Text generation model
    "gpt-4o",  # Text generation model
    "gpt-4",  # Text generation model
    "gpt-3.5-turbo",  # Text generation model
    "claude-3.5-sonnet",  # Text generation model
    "unity"  # Hybrid model (used as a text model in this case)
]

# Function for handling text generation
def gpt_text_response(prompt, selected_model):
    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content  # Text response
    except Exception as e:
        return f"An error occurred with G4F API: {e}"  # Error message

# Apply custom CSS for a modern card-based UI
st.markdown(
    """
    <style>
        /* General body styling */
        .stApp {
            background-color: #f5f7fa;
            font-family: 'Roboto', sans-serif;
        }

        /* Center container styling */
        .main-container {
            max-width: 900px;
            margin: 50px auto;
            padding: 2rem;
            border-radius: 15px;
            background: white;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        /* Title and subtitle */
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

        /* Card-like input areas */
        .input-card {
            background: #e3f2fd;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        textarea, select {
            font-size: 16px !important;
            border-radius: 8px !important;
            padding: 12px !important;
            width: 100%;
        }

        /* Button styling */
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

        /* Response box */
        .response-card {
            background: #f1f8e9;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            font-size: 16px;
            color: #333;
            font-weight: 500;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout setup
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title and subtitle
st.markdown('<h1 class="title">🚀 Modern AI Text Generator</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">A sleek, card-based interface for generating text using advanced AI models.</p>',
    unsafe_allow_html=True,
)

# Input area card
st.markdown('<div class="input-card">', unsafe_allow_html=True)
prompt = st.text_area(
    "Enter your prompt:",
    placeholder="Type something creative...",
    height=150,
)
selected_model = st.selectbox(
    "Select a model:",
    options=available_models,
)
st.markdown('</div>', unsafe_allow_html=True)

# Button and AI response
if st.button("Generate AI Response"):
    if not prompt.strip():
        st.error("⚠️ Please provide a valid prompt!")
    else:
        with st.spinner("🔄 Generating your response..."):
            response = gpt_text_response(prompt, selected_model)
        
        # Display the response inside a card
        st.markdown('<div class="response-card">', unsafe_allow_html=True)
        st.write(response)
        st.markdown('</div>', unsafe_allow_html=True)

# Closing container
st.markdown('</div>', unsafe_allow_html=True)
