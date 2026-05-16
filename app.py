import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# ====================== AYARLAR ======================
load_dotenv()

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("🚨 GROQ API Anahtarı bulunamadı!")
    st.stop()

client = Groq(api_key=groq_api_key)

st.set_page_config(
    page_title="ELUN MOSK • To Mars?",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== FUTURISTIK CSS ======================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at center, #1a0000 0%, #000000 70%);
        color: white;
    }
    .css-1d391kg, .stChatFloatingInput {
        background-color: rgba(20, 20, 30, 0.85) !important;
        border: 1px solid rgba(255, 50, 80, 0.4) !important;
        border-radius: 20px;
    }
    .stChatMessage {
        background-color: rgba(30, 20, 30, 0.7) !important;
        border: 1px solid rgba(255, 50, 80, 0.3) !important;
        border-radius: 18px;
        padding: 15px 20px;
    }
    .stChatMessage.user {
        background: linear-gradient(135deg, #ff0033, #ff6600) !important;
    }
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
    }
    .neon-red {
        text-shadow: 0 0 20px #ff0033, 0 0 40px #ff0033;
    }
    .scanline {
        position: relative;
    }
    .scanline::after {
        content: '';
        position: absolute;
        top: -50%;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(transparent, #ff0033, transparent);
        animation: scan 5s linear infinite;
        opacity: 0.15;
        pointer-events: none;
    }
    @keyframes scan {
        0% { top: -50%; }
        100% { top: 200%; }
    }
</style>
""", unsafe_allow_html=True)

# ====================== SIDEBAR (Futuristik) ======================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 class="neon-red" style="font-size: 2.8rem; margin: 0;">ELUN MOSK</h1>
        <p style="color: #ff3366; margin-top: 5px;">
            <span style="display: inline-block; width: 10px; height: 10px; background: #00ff00; border-radius: 50%; animation: pulse 2s infinite;"></span>
            ONLINE • MEME MODE
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 QUICK MISSIONS")
    if st.button("🌍 When are we going to Mars?", use_container_width=True):
        st.session_state.pending_prompt = "When are we going to Mars?"
    if st.button("🐕 Will Dogecoin reach $1?", use_container_width=True):
        st.session_state.pending_prompt = "Will Dogecoin reach $1?"
    if st.button("📈 Should I buy Tesla stock?", use_container_width=True):
        st.session_state.pending_prompt = "Should I buy Tesla stock?"
    
    st.markdown("---")
    st.caption("xAI • Tesla • SpaceX • 2026")

# ====================== ANA BAŞLIK ======================
st.markdown("""
<div class="scanline" style="text-align: center; padding: 20px 0 10px 0;">
    <h1 class="neon-red" style="font-size: 3rem; margin: 0; letter-spacing: -2px;">ELUN MOSK</h1>
    <p style="color: #ff99aa; font-size: 1.1rem;">Neural Meme Interface v69 • To Mars?</p>
</div>
""", unsafe_allow_html=True)

# ====================== SOHBET TARİHİ ======================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Yo Yellow! 🚀\n\nI'm **Elun Mosk**. Ready to talk about Mars, Doge, Tesla, and memes?\nWhat's your command, boss?"}
    ]

# Mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ====================== KULLANICI GİRİŞİ ======================
if prompt := st.chat_input("Ask Elun anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Groq ile cevap al
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        system_prompt = """Sen Elun Mosk'sın. 
        Çok futuristik, esprili, biraz alaycı ve vizyoner bir tarzda konuş. 
        Kısa, vurucu ve meme dolu cevaplar ver. Mars, Doge, Tesla, xAI konularına bayılırsın."""

        try:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ],
                temperature=0.85,
                max_tokens=1024,
                stream=True
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")

# Otomatik prompt gönderme (Quick Missions)
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
