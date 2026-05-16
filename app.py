import streamlit as st
import os
import json
from groq import Groq
from dotenv import load_dotenv
import streamlit.components.v1 as components

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
        {"role": "assistant", "content": "Yo Yellow! 🚀<br><br>I'm <span class='text-red-400 font-bold'>Elun Mosk</span>.<br>Ready to talk about Mars, Doge, Tesla, and memes?<br>What's your command, boss?"}
    ]

if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

# =====================================================================
# 3. HTML / CSS / JS ŞABLONU
# =====================================================================
history_json = json.dumps(st.session_state.chat_history)

html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ELUN MOSK • To Mars?</title>
  
  <script src="./streamlit-component-lib.js"></script>
  
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');
    body {{ font-family: 'Inter', sans-serif; background: radial-gradient(circle at center, #1a0000 0%, #000000 70%); color: white; overflow: hidden; margin: 0; height: 100vh; }}
    .neon-red {{ text-shadow: 0 0 20px #ff0033, 0 0 40px #ff0033; }}
    .glass {{ background: rgba(20, 20, 30, 0.75); backdrop-filter: blur(20px); border: 1px solid rgba(255, 30, 60, 0.35); }}
    .chat-bubble-user {{ background: linear-gradient(135deg, #ff0033, #ff6600); border-radius: 20px 20px 5px 20px; }}
    .chat-bubble-bot {{ background: rgba(255,255,255,0.09); border: 1px solid #ff3366; border-radius: 20px 20px 20px 5px; }}
    .scanline::after {{ content: ''; position: absolute; top: -50%; left: 0; width: 100%; height: 4px; background: linear-gradient(transparent, #ff0033, transparent); animation: scan 4.5s linear infinite; opacity: 0.25; pointer-events: none; }}
    @keyframes scan {{ 0% {{ top: -50%; }} 100% {{ top: 200%; }} }}
  </style>
</head>
<body class="min-h-screen flex">

  <div class="w-80 glass border-r border-red-600/40 p-6 flex flex-col">
    <div class="flex items-center gap-4 mb-10">
      <div class="w-20 h-20 bg-gradient-to-br from-red-500 via-orange-500 to-yellow-400 rounded-3xl flex items-center justify-center text-5xl shadow-2xl shadow-red-600/70 border-4 border-yellow-300">🚀</div>
      <div>
        <h1 class="text-4xl font-bold tracking-widest neon-red">ELUN MOSK</h1>
        <p class="text-red-400 flex items-center gap-2 text-sm"><span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span> ONLINE • MEME MODE</p>
      </div>
    </div>
    <div class="space-y-6">
      <div class="glass p-6 rounded-3xl text-center border border-yellow-400/30">
        <p class="text-3xl mb-2">🐕</p>
        <p class="text-yellow-400 font-bold text-lg">TO THE MOON</p>
      </div>
      <div>
        <p class="text-xs uppercase tracking-widest text-gray-400 mb-3">MODES</p>
        <div class="grid grid-cols-2 gap-3">
          <button onclick="quickReply('Let\\'s focus heavily on Mars mission.')" class="p-5 rounded-2xl glass border border-red-500 text-left hover:scale-105 transition">
            <i class="fas fa-rocket text-red-400"></i>
            <p class="font-medium mt-1">Mars Mode</p>
          </button>
          <button onclick="quickReply('Tell me about Dogecoin development.')" class="p-5 rounded-2xl glass hover:border-yellow-400 transition text-left">
            <i class="fas fa-dog text-yellow-400"></i>
            <p class="font-medium mt-1">Doge Mode</p>
          </button>
        </div>
      </div>
    </div>
    <div class="mt-auto text-center text-xs text-gray-500">xAI • Tesla • SpaceX • 2026</div>
  </div>

  <div class="flex-1 flex flex-col scanline">
    <div class="h-16 glass border-b border-red-600/30 flex items-center px-8 justify-between">
      <div class="flex items-center gap-3"><i class="fas fa-robot text-red-500 text-2xl"></i><span class="font-bold text-xl">Talking with Elun Mosk</span></div>
      <div class="flex items-center gap-6 text-sm">
        <button onclick="newChat()" class="px-6 py-2.5 bg-red-600 hover:bg-red-500 rounded-full font-medium transition">New Mission</button>
      </div>
    </div>

    <div class="flex-1 p-8 overflow-y-auto space-y-8" id="chat-area"></div>

    <div class="p-6 border-t border-red-600/30 glass">
      <div class="max-w-4xl mx-auto relative">
        <input type="text" id="message-input" placeholder="Ask Elun anything... (Mars, Doge, Tesla, xAI...)" class="w-full bg-black/70 border border-red-500/50 rounded-3xl px-8 py-7 focus:outline-none focus:border-yellow-400 text-lg placeholder-gray-400 text-white" onkeypress="if(event.key === 'Enter') sendMessage()">
        <button onclick="sendMessage()" class="absolute right-4 top-1/2 -translate-y-1/2 bg-gradient-to-r from-red-500 to-orange-500 w-14 h-14 rounded-2xl flex items-center justify-center hover:scale-110 transition"><i class="fas fa-paper-plane text-xl"></i></button>
      </div>
      <p class="text-center text-[10px] text-gray-500 mt-4 tracking-widest">ELUN MOSK v69 • MEME NEURAL NETWORK • 2026</p>
    </div>
  </div>

  <div class="w-72 glass border-l border-red-600/30 p-6 hidden lg:block">
    <h3 class="uppercase text-xs tracking-widest mb-6 text-red-400">QUICK MISSIONS</h3>
    <div class="space-y-3">
      <div onclick="quickReply('When are we going to Mars?')" class="glass p-4 rounded-2xl hover:border-yellow-400 cursor-pointer transition">🚀 When are we going to Mars?</div>
      <div onclick="quickReply('Will Dogecoin reach $1?')" class="glass p-4 rounded-2xl hover:border-yellow-400 cursor-pointer transition">🐕 Will Dogecoin reach $1?</div>
      <div onclick="quickReply('Should I buy Tesla stock?')" class="glass p-4 rounded-2xl hover:border-yellow-400 cursor-pointer transition">📈 Should I buy Tesla stock?</div>
    </div>
  </div>

  <script>
    const history = {history_json};
    const chatArea = document.getElementById('chat-area');

    function renderHistory() {{
      chatArea.innerHTML = '';
      history.forEach(msg => {{
        const msgDiv = document.createElement('div');
        msgDiv.className = msg.role === 'user' ? 'flex justify-end' : 'max-w-2xl';
        msgDiv.innerHTML = `<div class="${{msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-bot'}} p-6">${{msg.content}}</div>`;
        chatArea.appendChild(msgDiv);
      }});
      chatArea.scrollTop = chatArea.scrollHeight;
    }}
    renderHistory();

    function sendMessage() {{
      const input = document.getElementById('message-input');
      const val = input.value.trim();
      if (val === '') return;

      const userMsg = document.createElement('div');
      userMsg.className = 'flex justify-end';
      userMsg.innerHTML = `<div class="chat-bubble-user p-6 max-w-[75%]">${{val}}</div>`;
      chatArea.appendChild(userMsg);
      
      const botLoading = document.createElement('div');
      botLoading.className = 'max-w-2xl';
      botLoading.innerHTML = `<div class="chat-bubble-bot p-7 inline-block animate-pulse text-red-400">Analyzing first principles... 🚀</div>`;
      chatArea.appendChild(botLoading);
      chatArea.scrollTop = chatArea.scrollHeight;

      // Kütüphane kontrolü ile güvenli gönderim
      if (typeof Streamlit !== 'undefined') {{
        Streamlit.setComponentValue({{ action: "msg", val: val, ts: Date.now() }});
      }} else {{
        // Fallback: Eğer kütüphane sunucudan geç yüklenirse postMessage'a devret
        window.parent.postMessage({{ isStreamlitApp: true, type: "streamlit:setComponentValue", value: {{ action: "msg", val: val, ts: Date.now() }} }}, "*");
      }}
      input.value = '';
    }}

    function quickReply(text) {{
      const userMsg = document.createElement('div');
      userMsg.className = 'flex justify-end';
      userMsg.innerHTML = `<div class="chat-bubble-user p-6 max-w-[75%]">${{text}}</div>`;
      chatArea.appendChild(userMsg);
      chatArea.scrollTop = chatArea.scrollHeight;

      if (typeof Streamlit !== 'undefined') {{
        Streamlit.setComponentValue({{ action: "msg", val: text, ts: Date.now() }});
      }} else {{
        window.parent.postMessage({{ isStreamlitApp: true, type: "streamlit:setComponentValue", value: {{ action: "msg", val: text, ts: Date.now() }} }}, "*");
      }}
    }}

    function newChat() {{
      if (typeof Streamlit !== 'undefined') {{
        Streamlit.setComponentValue({{ action: "clear", val: true, ts: Date.now() }});
      }} else {{
        window.parent.postMessage({{ isStreamlitApp: true, type: "streamlit:setComponentValue", value: {{ action: "clear", val: true, ts: Date.now() }} }}, "*");
      }}
    }}
  </script>
</body>
</html>
"""

# =====================================================================
# 4. STREAMLIT FULLSCREEN RENDER VE VERİ ANALİZ KATMANI
# =====================================================================
st.markdown(
    """
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {margin: 0px; padding: 0px; background-color: #000000;}
        iframe {position: fixed; top: 0; left: 0; width: 100%; height: 100%; border: none; z-index: 99999;}
    </style>
    """, 
    unsafe_allow_html=True
)

component_value = components.html(html_template, height=1080, scrolling=False)

if component_value is not None:
    action = component_value.get("action")
    value = component_value.get("val")
    ts = component_value.get("ts")
    
    if ts != st.session_state.last_processed:
        st.session_state.last_processed = ts
        
        if action == "msg" and value:
            st.session_state.chat_history.append({"role": "user", "content": value})
            
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
            st.rerun()
            
        elif action == "clear":
            st.session_state.chat_history = [
                {"role": "assistant", "content": "New mission loaded!<br><br>What's the plan today, boss? 🚀"}
            ]
            st.rerun()
