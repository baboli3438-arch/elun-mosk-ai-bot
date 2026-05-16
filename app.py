import streamlit as st
import os
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
    st.error("🚨 API Anahtarı Bulunamadı! Lütfen .env dosyasını veya Streamlit Secrets ayarlarını kontrol edin.")
    st.stop()

client = Groq(api_key=groq_api_key)

# =====================================================================
# 2. SOHBET GEÇMİŞİ VE STATE YÖNETİMİ
# =====================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Yo, what's up? 🚀<br><br>I'm <span class='text-red-400 font-bold'>Elun Mosk</span>.<br>Ready to talk about Mars, Doge, Tesla, and memes?<br>What's your command, boss?"}
    ]

# =====================================================================
# 3. GLOBAL SİBERPUNK CSS GÖMME
# =====================================================================
st.markdown(
    """
    <style>
        /* Streamlit varsayılan başlık ve altlıklarını gizle */
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {background-color: #000000; margin: 0; padding: 0;}
        .block-container {padding: 0rem !important; max-width: 100% !important;}
        
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');
        
        /* Layout Yapısı */
        .main-layout {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at center, #1a0000 0%, #000000 70%);
            color: white;
            display: flex;
            height: 100vh;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
        }
        .neon-red { text-shadow: 0 0 20px #ff0033, 0 0 40px #ff0033; }
        .glass { background: rgba(20, 20, 30, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(255, 30, 60, 0.35); }
        
        /* Baloncuk Tasarımları */
        .chat-container {
            flex: 1; display: flex; flex-col: column; padding: 2rem; 
            overflow-y: auto; height: calc(100vh - 14rem); space-y: 2rem;
        }
        .chat-bubble-user { background: linear-gradient(135deg, #ff0033, #ff6600); border-radius: 20px 20px 5px 20px; padding: 1.25rem; max-width: 70%; margin-left: auto; margin-bottom: 1rem; text-align: left; color: white;}
        .chat-bubble-bot { background: rgba(255,255,255,0.09); border: 1px solid #ff3366; border-radius: 20px 20px 20px 5px; padding: 1.5rem; max-width: 70%; margin-right: auto; margin-bottom: 1rem; display: inline-block; color: white;}
        
        /* Streamlit Chat Input Alanını Koda Gömme ve Stilize Etme */
        .stChatInput {
            position: fixed; bottom: 3rem; left: 22rem; right: 20rem; z-index: 1000;
            background: rgba(0, 0, 0, 0.8) !important;
            border: 1px solid rgba(255, 0, 51, 0.5) !important;
            border-radius: 2rem !important;
        }
        .stChatInput textarea {
            background: transparent !important; color: white !important; font-size: 1.1rem !important;
        }
        
        .scanline::after { content: ''; position: absolute; top: -50%; left: 0; width: 100%; height: 4px; background: linear-gradient(transparent, #ff0033, transparent); animation: scan 4.5s linear infinite; opacity: 0.15; pointer-events: none; }
        @keyframes scan { 0% { top: -50%; } 100% { top: 200%; } }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 4. YETENEK & TETİKLEME FONKSİYONU
# =====================================================================
def handle_chat_request(user_message):
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    
    system_prompt = (
        "Sen Elun Mosk'sın. HTML tasarımındaki gibi tamamen fütüristik, Mars odaklı, "
        "Dogecoin hayranı, hafif alaycı, esprili ve vizyoner bir tarzda konuş. "
        "Yanıtlarını İngilizce olarak ver, kısa, öz ve vurucu tut. Mühendislik ve meme odaklı ol."
    )
    
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "system", "content": system_prompt}, *st.session_state.chat_history]
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = f"Mission Error: {str(e)} 🚀"
        
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# =====================================================================
# 5. EKRAN RENDER SÜRECİ
# =====================================================================
chat_html_content = ""
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        chat_html_content += f'<div class="flex justify-end"><div class="chat-bubble-user">{msg["content"]}</div></div>'
    else:
        chat_html_content += f'<div class="max-w-2xl"><div class="chat-bubble-bot">{msg["content"]}</div></div>'

# Sol Menü ve İskelet Enjeksiyonu
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

    <div class="flex-1 p-8 overflow-y-auto" style="padding-bottom: 12rem; height: calc(100vh - 10rem);">
        {chat_html_content}
    </div>
    
    <div class="absolute bottom-0 left-0 w-full h-40 border-t border-red-600/30 glass" style="z-index: 10;">
        <p class="text-center text-[10px] text-gray-500 pt-28 tracking-widest">DS2LL4PuC4Hc1cDhXe5eZf7YxNmoUxY628 • DOGECOIN ONLY</p>
    </div>
  </div>
  
  <div class="w-72 glass border-l border-red-600/30 p-6 hidden lg:block">
    <h3 class="uppercase text-xs tracking-widest mb-6 text-red-400">QUICK MISSIONS</h3>
    <div class="space-y-3 text-sm text-gray-300">
      <div class="glass p-4 rounded-2xl border border-red-500/20">🚀 Mars Mission Beta</div>
      <div class="glass p-4 rounded-2xl border border-red-500/20">🐕 Dogecoin Orbit</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Streamlit'in kendi güvenli input mekanizmasını ekliyoruz
user_query = st.chat_input("Ask Elun anything... (Mars, Doge, Tesla...)")
if user_query:
    handle_chat_request(user_query)
    st.rerun()
