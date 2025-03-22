import streamlit as st
import g4f
import os

# Configurar o provedor Blackbox
client = g4f.ChatCompletion.create

# Modelos disponíveis
available_models = [
    "o1",
    "o3-mini",
    "deepseek-r1",
    "gpt-4o",
    "claude-3.7-sonnet"
]

# Função para processar respostas
def gpt_response(prompt, selected_model, images=None):
    try:
        if images:
            # Salvar imagens no diretório
            image_dir = "uploaded_images"
            os.makedirs(image_dir, exist_ok=True)
            saved_images = []
            for image in images:
                file_path = os.path.join(image_dir, image.name)
                with open(file_path, "wb") as f:
                    f.write(image.getbuffer())
                saved_images.append(file_path)

            # Resposta com imagens
            response = client(
                provider=g4f.Provider.Blackbox,
                model=selected_model,
                messages=[{"role": "user", "content": prompt}],
                images=saved_images
            )
        else:
            # Resposta apenas de texto
            response = client(
                provider=g4f.Provider.Blackbox,
                model=selected_model,
                messages=[{"role": "user", "content": prompt}]
            )
        return response if response else "❌ Erro ao obter resposta da IA"
    except Exception as e:
        return f"⚠️ Erro: {e}"

# Aplicar CSS para UI moderna
st.markdown(
    """
    <style>
        .stApp { background-color: #f5f7fa; font-family: 'Roboto', sans-serif; }
        .main-container { max-width: 900px; margin: 50px auto; padding: 2rem; border-radius: 15px; background: white; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); }
        .title { font-size: 2.5rem; font-weight: 700; color: #1a73e8; text-align: center; }
        .subtitle { font-size: 1.1rem; color: #333; text-align: center; margin-bottom: 2rem; }
        .input-card { background: #e3f2fd; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); }
        textarea, select, input { font-size: 16px !important; border-radius: 8px !important; padding: 12px !important; width: 100%; }
        .stButton > button { background-color: #1a73e8; color: white; border: none; border-radius: 8px; font-size: 16px; padding: 12px 24px; transition: 0.3s; cursor: pointer; }
        .stButton > button:hover { background-color: #1558b0; }
        .response-card { background: #f1f8e9; border-radius: 10px; padding: 20px; margin-top: 20px; font-size: 16px; color: #333; font-weight: 500; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); white-space: pre-wrap; }
        .message-container { margin-bottom: 1.5rem; }
        .user-message { padding: 10px; border-radius: 8px; background-color: #d1e8ff; max-width: 80%; margin: 5px 0; }
        .bot-message { padding: 10px; border-radius: 8px; background-color: #f1f8e9; max-width: 80%; margin: 5px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Título e subtítulo
st.markdown('<h1 class="title">🚀 Modern AI Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Envie texto e imagens para interagir com IA!</p>', unsafe_allow_html=True)

# Área de entrada
st.markdown('<div class="input-card">', unsafe_allow_html=True)
prompt = st.text_area("Digite sua mensagem:", placeholder="Digite sua pergunta aqui...", height=150)
selected_model = st.selectbox("Selecione o modelo:", available_models)

# Upload de imagens
uploaded_images = st.file_uploader("Envie imagens:", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)

# Histórico de chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Exibir mensagens antigas
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f'<div class="message-container"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)
    elif message["role"] == "bot":
        st.markdown(f'<div class="message-container"><div class="bot-message">{message["content"]}</div></div>', unsafe_allow_html=True)

# Botão de envio
if st.button("Enviar"):
    if not prompt.strip():
        st.error("⚠️ Digite uma mensagem antes de enviar!")
    else:
        # Salvar mensagem do usuário
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Obter resposta
        response = gpt_response(prompt, selected_model, uploaded_images)

        # Adicionar resposta ao histórico
        st.session_state.chat_history.append({"role": "bot", "content": response}) 
