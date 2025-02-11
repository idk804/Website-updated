import streamlit as st
import g4f
import g4f.Provider
from PIL import Image

# --------------------------------------
# Functions for interacting with g4f APIs
# --------------------------------------

def gpt_text_response_stream(prompt, selected_model):
    """
    Stream text responses using g4f with a text-only model (streaming).
    """
    client = g4f.Client()
    try:
        stream = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,  # Enable streaming
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"An error occurred: {e}"


def gpt_text_response_no_stream(prompt, selected_model):
    """
    Retrieve the text response for a given prompt without streaming.
    (Used for the "evil" model.)
    """
    client = g4f.Client()
    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            stream=False  # Disable streaming
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


def chat_completion_vision(prompt, uploaded_images):
    """
    Send a prompt along with one or more images to a vision-enabled text model.
    This example uses the Blackbox provider.
    """
    client = g4f.Client(provider=g4f.Provider.Blackbox)
    images = []
    for uploaded_file in uploaded_images:
        images.append([uploaded_file, uploaded_file.name])
    try:
        response = client.chat.completions.create(
            [{"content": prompt, "role": "user"}],
            "",
            images=images
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred during vision chat completion: {e}"


# --------------------------------------
# Custom CSS for Modern UI
# --------------------------------------
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

# --------------------------------------
# Main App Layout
# --------------------------------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">🚀 Modern AI App with Vision</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Select a mode to generate text or use vision-enabled text models.</p>',
    unsafe_allow_html=True,
)

# Choose the operating mode
mode = st.radio("Select Mode:", options=["Text Generation", "Image Reading", "Vision Mode"])

# -----------------------
# Mode: Text Generation
# -----------------------
if mode == "Text Generation":
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    prompt = st.text_area("Enter your prompt:", placeholder="Type something creative...", height=150)
    st.markdown('</div>', unsafe_allow_html=True)

    # Updated list of available text generation models
    available_text_models = [
        "deepseek-r1",
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-4",
        "gpt-3.5-turbo",
        "claude-3.5-sonnet",
        "evil"  # "evil" will be processed without streaming
    ]
    selected_model = st.selectbox("Select a model:", options=available_text_models)

    if st.button("Generate Text Response"):
        if not prompt.strip():
            st.error("⚠️ Please enter a valid prompt!")
        else:
            st.markdown('<div class="response-card">', unsafe_allow_html=True)
            with st.spinner("🔄 Generating text response..."):
                # If the selected model is "evil", use the non-streaming function.
                if selected_model == "evil":
                    result = gpt_text_response_no_stream(prompt, selected_model)
                    st.write(result)
                else:
                    response_container = st.empty()
                    full_response = ""
                    for chunk in gpt_text_response_stream(prompt, selected_model):
                        full_response += chunk
                        response_container.markdown(full_response)
            st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# Mode: Image Reading
# -----------------------
elif mode == "Image Reading":
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.write(f"Image size: {image.size[0]} x {image.size[1]} pixels")
        except Exception as e:
            st.error(f"Error reading the image: {e}")

# -----------------------
# Mode: Vision Mode (Text + Images)
# -----------------------
else:  # Vision Mode
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    prompt = st.text_area("Enter your prompt for vision model:", placeholder="Ask something about the images...", height=150)
    uploaded_images = st.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Generate Vision Response"):
        if not prompt.strip():
            st.error("⚠️ Please enter a valid prompt!")
        elif not uploaded_images:
            st.error("⚠️ Please upload at least one image!")
        else:
            with st.spinner("🔄 Generating vision-enabled response..."):
                result = chat_completion_vision(prompt, uploaded_images)
            st.markdown('<div class="response-card">', unsafe_allow_html=True)
            st.write(result)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
