import streamlit as st
import os
import json
from groq import Groq
from dotenv import load_dotenv

# =====================================================================
# 1. GÜVENLİK VE API AYARLARI
# =====================================================================
load_dotenv()
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("🚨 API Anahtarı Bulunamadı! Lütfen Streamlit Dashboard > Settings > Secrets ayarlarını kontrol edin.")
    st.stop()

client = Groq(api_key=groq_api_key)

# =====================================================================
# 2. SOHBET GEÇMİŞİ VE STATE YÖNETİMİ
# =====================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Yo bro! 🚀<br><br>I'm <span class='text-red-400 font-bold'>Elun Mosk</span>.<br>Ready to talk about Mars, Doge, Tesla, and memes?<br>What's your command, boss?"}
    ]

# Hızlı butonlar veya New Mission tetiklemeleri için kontrol
if "quick_input" not in st.session_state:
    st.session_state.quick_input = ""

# =====================================================================
# 3. DIŞ CSS GÖMME (STREAMLIT ELEMANLARINI ÖZELLEŞTİRME VE GİZLEME)
# =====================================================================
st.markdown(
    """
    <style>
        /* Streamlit varsayılan arayüzünü gizle */
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {background-color: #000000; margin: 0; padding: 0;}
        .block-container {padding-top: 0rem; padding-bottom: 0rem; max-width: 100% !important;}
        
        /* HTML Tasarım Temelleri */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');
        
        .main-layout {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at center, #1a0000 0%, #000000 70%);
            color: white;
            display: flex;
            min-height: 100vh;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
        }
        .neon-red { text-shadow: 0 0 20px #ff0033, 0 0 40px #ff0033; }
        .glass { background: rgba(20, 20, 30, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(255, 30, 60, 0.35); }
        .chat-bubble-user { background: linear-gradient(135deg, #ff0033, #ff6600); border-radius: 20px 20px 5px 20px; padding: 1.5rem; max-width: 75%; margin-left: auto; margin-bottom: 1.5rem; text-align: left;}
        .chat-bubble-bot { background: rgba(255,255,255,0.09); border: 1px solid #ff3366; border-radius: 20px 20px 20px 5px; padding: 1.75rem; max-width: 75%; margin-right: auto; margin-bottom: 1.5rem; display: inline-block;}
        .scanline::after { content: ''; position: absolute; top: -50%; left: 0; width: 100%; height: 4px; background: linear-gradient(transparent, #ff0033, transparent); animation: scan 4.5s linear infinite; opacity: 0.25; pointer-events: none; }
        @keyframes scan { 0% { top: -50%; } 100% { top: 200%; } }
        
        /* Streamlit Formunu Sayfanın Altındaki Input Alanına Tam Oturtma */
        .stForm {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 auto !important;
            max-width: 56rem;
        }
        /* Streamlit Girdi Kutusunu fütüristik yapma */
        .stTextInput input {
            background-color: rgba(0, 0, 0, 0.7) !important;
            border: 1px solid rgba(255, 0, 51, 0.5) !important;
            border-radius: 1.5rem !important;
            color: white !important;
            padding: 1.5rem 2rem !important;
            font-size: 1.125rem !important;
        }
        .stTextInput input:focus {
            border-color: #facc15 !important;
            box-shadow: 0 0 15px rgba(250, 204, 21, 0.4) !important;
        }
        /* Gönder butonunu özelleştirme */
        .stButton button {
            background: linear-gradient(to right, #ff0033, #ff6600) !important;
            color: white !important;
            border: none !important;
            border-radius: 1rem !important;
            padding: 0.75rem 2rem !important;
            font-weight: bold !important;
            transition: transform 0.2s !important;
        }
        .stButton button:hover {
            transform: scale(1.05) !important;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 4. FORM TETİKLENME VE YAPAY ZEKA MANTIĞI
# =====================================================================
def process_message(user_text):
    if user_text.strip() == "":
        return
    st.session_state.chat_history.append({"role": "user", "content": user_text})
    
    system_prompt = (
        "Sen Elun Mosk'sın. Fütüristik, Mars odaklı, Dogecoin hayranı, "
        "hafif alaycı, esprili ve vizyoner bir tarzda konuş. Yanıtların kısa, "
        "öz, vurucu ve kesinlikle İngilizce olsun. Mühendislik ve meme odaklı yaklaş."
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": system_prompt}, *st.session_state.chat_history]
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = f"Neural link timeout: {str(e)} 🚀"
        
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Sidebar üzerindeki veya sağ paneldeki butonların tıklama kontrolleri
if st.sidebar.button("🚀 Mars Mode"):
    process_message("Let's focus heavily on Mars mission.")
if st.sidebar.button("🐕 Doge Mode"):
    process_message("Tell me about Dogecoin development.")
if st.sidebar.button("♻️ New Mission", type="primary"):
    st.session_state.chat_history = [{"role": "assistant", "content": "New mission loaded!<br><br>What's the plan today, boss? 🚀"}]
    st.rerun()

# =====================================================================
# 5. ARAYÜZ KATMANLARININ BİRLEŞTİRİLMESİ
# =====================================================================

# Mesaj alanının HTML string yapısı
chat_html_content = ""
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        chat_html_content += f'<div class="flex justify-end"><div class="chat-bubble-user">{msg["content"]}</div></div>'
    else:
        chat_html_content += f'<div class="max-w-2xl"><div class="chat-bubble-bot">{msg["content"]}</div></div>'

# Sayfa İskeleti
st.markdown(f"""
<div class="main-layout">
  <div class="w-80 glass border-r border-red-600/40 p-6 flex flex-col hidden md:flex">
    <div class="flex items-center gap-4 mb-10">
      <div class="w-20 h-20 bg-gradient-to-br from-red-500 via-orange-500 to-yellow-400 rounded-3xl flex items-center justify-center text-5xl border-4 border-yellow-300">🚀</div>
      <div>
        <h1 class="text-4xl font-bold tracking-widest neon-red">ELUN MOSK</h1>
        <p class="text-red-400 flex items-center gap-2 text-sm"><span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span> ONLINE</p>
      </div>
    </div>
    <div class="glass p-6 rounded-3xl text-center border border-yellow-400/30 mb-6">
        <p class="text-3xl mb-2">🐕</p>
        <p class="text-yellow-400 font-bold text-lg">TO THE MOON</p>
    </div>
    <div class="mt-auto text-center text-xs text-gray-500">xAI • Tesla • SpaceX • 2026</div>
  </div>

  <div class="flex-1 flex flex-col scanline relative" style="height: 100vh;">
    <div class="h-16 glass border-b border-red-600/30 flex items-center px-8 justify-between">
      <div class="flex items-center gap-3"><i class="fas fa-robot text-red-500 text-2xl"></i><span class="font-bold text-xl">Talking with Elun Mosk</span></div>
    </div>

    <div class="flex-1 p-8 overflow-y-auto space-y-8" style="padding-bottom: 12rem;">
        {chat_html_content}
    </div>
    
    <div class="absolute bottom-0 left-0 w-full p-6 border-t border-red-600/30 glass z-50">
        </div>
</div>
""", unsafe_allow_html=True)

# Streamlit Formunu Tam Alt Kısımdaki Konteyner İçine Yerleştiriyoruz
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        cols = st.columns([0, 8, 2, 0]) # Kenar boşlukları ile ortalama
        with cols[1]:
            user_input = st.text_input(
                label="Message input",
                placeholder="Ask Elun anything... (Mars, Doge, Tesla...)",
                label_visibility="collapsed"
            )
        with cols[2]:
            submit_button = st.form_submit_button(label="SEND 🚀")
            
        if submit_button and user_input:
            process_message(user_input)
            st.rerun()

st.markdown("<p class='text-center text-[10px] text-gray-500 tracking-widest' style='position: fixed; bottom: 5px; width: 100%; text-align: center; z-index: 100;'>ELUN MOSK v69 • 2026</p>", unsafe_allow_html=True)
