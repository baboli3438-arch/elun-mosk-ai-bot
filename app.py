import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# =====================================================================
# 1. SAYFA VE GENİŞLİK YAPILANDIRMASI
# =====================================================================
st.set_page_config(
    page_title="ELUN MOSK • To Mars?", 
    page_icon="🚀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# =====================================================================
# 2. GÖRSELDEKİ ARAYÜZÜ BİREBİR SAĞLAYAN SİBERPUNK CSS ENJEKSİYONU
# =====================================================================
st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;600&display=swap');
    
    /* Global Arka Plan: Görseldeki Radyal Koyu Kırmızı ve Siyah */
    .stApp {
        background: radial-gradient(circle at center, #1c0205 0%, #050001 80%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Streamlit Gereksiz Menüleri Gizleme */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 3 Panelli Düzen İçin Ana Taşıyıcı Efektleri */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 10, 12, 0.95) !important;
        border-right: 1px solid rgba(255, 48, 76, 0.25) !important;
    }
    
    /* Sol Panel Logo Bölümü */
    .brand-area {
        text-align: center;
        padding: 15px 0 30px 0;
        border-bottom: 1px solid rgba(255, 48, 76, 0.15);
        margin-bottom: 25px;
    }
    .brand-logo {
        font-size: 50px;
        background: linear-gradient(135deg, #ff3355, #ff6600, #ffcc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .brand-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        text-shadow: 0 0 15px #ff304c;
        letter-spacing: 3px;
        line-height: 1;
    }
    .brand-status {
        color: #ff4d6d;
        font-size: 11px;
        letter-spacing: 1.5px;
        margin-top: 6px;
    }
    .brand-status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        background-color: #00ff66;
        border-radius: 50%;
        margin-right: 5px;
        box-shadow: 0 0 8px #00ff66;
        animation: pulse 1.5s infinite;
    }
    
    /* Görseldeki "TO THE MOON" Bölümü */
    .moon-card {
        background: rgba(25, 15, 18, 0.6);
        border: 1px solid rgba(255, 204, 0, 0.3);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 0 15px rgba(255, 204, 0, 0.05);
    }
    .moon-card-title {
        color: #ffcc00;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 1.5px;
        margin-top: 5px;
    }
    
    /* Sohbet Baloncukları Özelleştirmesi (Görseldeki gibi Keskin ve İnce Kırmızı Çerçeveli) */
    .stChatMessage {
        background-color: rgba(18, 11, 13, 0.65) !important;
        border: 1px solid rgba(255, 48, 76, 0.25) !important;
        border-radius: 18px !important;
        padding: 18px !important;
        margin-bottom: 20px !important;
    }
    
    /* Kullanıcı Mesaj Baloncuğu (Görseldeki gibi Turuncu-Kırmızı Degrade) */
    [data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, #ff2a4b 0%, #ff6a00 100%) !important;
        border: none !important;
        color: white !important;
        border-radius: 18px 18px 4px 18px !important;
        margin-left: auto !important;
        max-width: 70%;
    }
    
    /* Input Alanı (Alt Çubuk ve Buton Entegrasyonu) */
    .stChatInputContainer {
        border: 1px solid rgba(255, 48, 76, 0.4) !important;
        background-color: #080305 !important;
        border-radius: 25px !important;
    }
    .stChatInputContainer textarea {
        color: #ffffff !important;
    }

    /* -----------------------------------------------------------------
       YENİ EKLENEN BUTON RENK VE YAZI DÜZELTME CSS ALANI
       ----------------------------------------------------------------- */
    /* Sağ paneldeki ve genel uygulamadaki tüm standart Streamlit butonlarını siberpunk tarzına zorla */
    div.stButton > button {
        background-color: rgba(25, 10, 15, 0.75) !important;
        color: #ff4d6d !important; /* Yazı rengi artık beyaz değil, parlak siberpunk kırmızısı */
        border: 1px solid rgba(255, 48, 76, 0.4) !important; /* İnce kırmızı çerçeve */
        border-radius: 12px !important;
        padding: 10px 15px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 0 8px rgba(255, 48, 76, 0.05) !important;
    }

    /* Butonların üzerine gelindiğinde (Hover durumu) */
    div.stButton > button:hover {
        background-color: rgba(255, 48, 76, 0.15) !important;
        color: #ffcc00 !important; /* Üzerine gelince yazılar Doge sarısına döner */
        border-color: #ff3355 !important;
        box-shadow: 0 0 15px rgba(255, 48, 76, 0.3) !important;
    }

    /* Butona tıklandığında veya odaklanıldığında beyaz blok oluşmasını engelle */
    div.stButton > button:active, div.stButton > button:focus {
        background-color: rgba(40, 10, 20, 0.9) !important;
        color: #ff4d6d !important;
        border-color: #ff3355 !important;
        box-shadow: 0 0 10px rgba(255, 48, 76, 0.4) !important;
    }
    
    /* Sol taraftaki Reset Mission (Primary) butonunun özel siberpunk degrade yapısı */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ff2a4b 0%, #ff6a00 100%) !important;
        color: white !important;
        border: none !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 20px rgba(255, 42, 75, 0.6) !important;
        color: white !important;
    }
    
    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 3. GÜVENLİ API VE AKTİF MODEL BAĞLANTISI (Llama 3.3 Motoru)
# =====================================================================
load_dotenv()
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("🚨 GROQ_API_KEY eksik! Lütfen secrets veya .env yapılandırmasını kontrol edin.")
    st.stop()

client = Groq(api_key=groq_api_key)

# =====================================================================
# 4. SOL PANEL (SIDEBAR) TASARIMI
# =====================================================================
with st.sidebar:
    st.markdown("""
        <div class="brand-area">
            <div class="brand-logo">🚀</div>
            <div class="brand-title">ELUN MOSK</div>
            <div class="brand-status"><span class="brand-status-dot"></span>ONLINE • MEME MODE</div>
        </div>
        
        <div class="moon-card">
            <div style="font-size: 28px;">🐕</div>
            <div class="moon-card-title">TO THE MOON</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("MODES")
    # State'leri tetikleyen temiz Streamlit butonları
    if st.button("🚀 Mars Mode", use_container_width=True):
        st.session_state.quick_trigger = "Let's focus heavily on Mars mission."
        
    if st.button("🐕 Doge Mode", use_container_width=True):
        st.session_state.quick_trigger = "Tell me about Dogecoin development."
        
    st.write("---")
    if st.button("💥 Reset Mission", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# =====================================================================
# 5. MERKEZİ CHAT EKRANI VE ANA AKIŞ
# =====================================================================
# Düzen düzenleme sütunları (Görseldeki yerleşimi bozmamak için dengeli dağılım)
chat_col, side_col = st.columns([3, 1])

with chat_col:
    st.markdown("### 🤖 Talking with Elun Mosk")
    
    # Hafıza havuzu oluşturma
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Yo, what's up? 🚀 I'm Elun Mosk. Ready to talk about Mars, Doge, Tesla, and memes?"
            }
        ]

    # Ekrandaki mesajları basma adımı
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Sağ panel "Quick Missions" alanı
with side_col:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("QUICK MISSIONS")
    if st.button("When are we going to Mars? 🚀", use_container_width=True):
        st.session_state.quick_trigger = "When are we going to Mars?"
    if st.button("Will Dogecoin reach $1? 🐕", use_container_width=True):
        st.session_state.quick_trigger = "Will Dogecoin reach $1?"
    if st.button("Should I buy Doge Coin? 📈", use_container_width=True):
        st.session_state.quick_trigger = "Should I buy Doge coin?"

# =====================================================================
# 6. GİRDİ YÖNETİMİ VE MODEL TETİKLEME ALANI
# =====================================================================
user_input = st.chat_input("Ask Elun anything... (Mars, Doge, Tesla...)")

# Eğer sağ veya sol panel butonlarına tıklandıysa girdiyi oradan yakala
if "quick_trigger" in st.session_state and st.session_state.quick_trigger:
    user_input = st.session_state.quick_trigger
    st.session_state.quick_trigger = None

if user_input:
    # Kullanıcı mesajını yerleştir
    with chat_col:
        with st.chat_message("user"):
            st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Karakter Tanımı (System Prompt)
    system_prompt = (
        "Sen Elun Mosk'sın. Tamamen fütüristik, Mars odaklı, Dogecoin hayranı, "
        "hafif alaycı, esprili ve vizyoner bir tarzda konuş. "
        "Yanıtlarını İngilizce olarak ver, kısa, öz ve vurucu tut. Mühendislik ve meme odaklı ol."
    )
    
    # İstek paketini hazırla
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
        
    with chat_col:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing first principles... 🚀"):
                try:
                    # Loglarında başarıyla çalışan en güncel kararlı model entegre edildi
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=api_messages
                    )
                    bot_response = completion.choices[0].message.content
                    st.markdown(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Mission Failure: {str(e)} 🚀")

# =====================================================================
# SEYFA SONU TELİF VE SİBERPUNK CÜZDAN BİLGİSİ (BELİRGİN SÜRÜM)
# =====================================================================
st.markdown("""
    <style>
    .footer-container {
        text-align: center;
        margin-top: 40px;
        padding: 20px 0;
        border-top: 1px solid rgba(255, 48, 76, 0.2);
        background: linear-gradient(to top, rgba(20, 0, 5, 0.8), transparent);
    }
    .footer-main-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 13px;
        font-weight: 700;
        color: #ff3355;
        text-shadow: 0 0 10px rgba(255, 51, 85, 0.6);
        letter-spacing: 2px;
        margin-bottom: 6px;
    }
    .footer-sub-text {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
        color: #ffffff;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.5);
        letter-spacing: 1.5px;
        opacity: 0.95;
    }
    </style>
    
    <div class="footer-container">
        <div class="footer-main-text">ELUN MOSK v69 • MEME NEURAL NETWORK • 2026</div>
        <div class="footer-sub-text">DS2LL4PuC4Hc1cDhXe5eZf7YxNmoUxY628 • DOGECOIN ONLY</div>
    </div>
""", unsafe_allow_html=True)
