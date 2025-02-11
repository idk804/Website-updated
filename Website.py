import streamlit as st
from g4f.client import Client
from PIL import Image

# Initialize the G4F client for text generation
client = Client()

# List of available models for text generation
available_text_models = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4",
    "gpt-3.5-turbo",
    "claude-3.5-sonnet",
    "unity"
]

# Function for streaming text response using g4f
def gpt_text_response_stream(prompt, selected_model):
    try:
        stream = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,  # Enable streaming
        )
        # Yield content chunk-by-chunk
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"An error occurred with G4F API: {e}"

# Custom CSS for a modern UI
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
            white-space: pre-wrap;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title and subtitle
st.markdown('<h1 class="title">🚀 Modern AI App</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Choose to generate text or read an image.</p>',
    unsafe_allow_html=True,
)

# Let the user choose the mode: Text Generation or Image Reading
mode = st.radio("Select Mode:", options=["Text Generation", "Image Reading"])

if mode == "Text Generation":
    # Text generation input
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    prompt = st.text_area(
        "Enter your prompt:",
        placeholder="Type something creative...",
        height=150,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    selected_model = st.selectbox(
        "Select a model:",
        options=available_text_models,
    )
    if st.button("Generate Text Response"):
        if not prompt.strip():
            st.error("⚠️ Please provide a valid prompt!")
        else:
            st.markdown('<div class="response-card">', unsafe_allow_html=True)
            response_container = st.empty()  # Placeholder for dynamic text content
            full_response = ""
            with st.spinner("🔄 Generating text response..."):
                for chunk in gpt_text_response_stream(prompt, selected_model):
                    full_response += chunk  # Append new chunks
                    response_container.markdown(full_response)  # Update display dynamically
            st.markdown('</div>', unsafe_allow_html=True)

else:  # Image Reading mode
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.write(f"Image size: {image.size[0]}x{image.size[1]} pixels")
            # You can add further image processing here if needed.
        except Exception as e:
            st.error(f"Error reading the image: {e}")

# Closing container
st.markdown('</div>', unsafe_allow_html=True)
