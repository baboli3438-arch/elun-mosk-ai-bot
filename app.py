import streamlit as st
import os
import json
from groq import Groq
from dotenv import load_dotenv
import streamlit.components.v1 as components

load_dotenv()

# ====================== API ======================
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("🚨 GROQ_API_KEY bulunamadı!")
    st.stop()

client = Groq(api_key=groq_api_key)

# ====================== SESSION STATE ======================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Yo, what's up? 🚀\n\nI'm Elun Mosk.\nReady to talk about Mars, Doge, Tesla, and memes?"}
    ]

if "last_message" not in st.session_state:
    st.session_state.last_message = None

# ====================== HANDLER ======================
def handle_chat_request(user_message: str):
    if not user_message or user_message == st.session_state.last_message:
        return
    
    st.session_state.last_message = user_message
    
    # Temiz tarihçe (HTML olmadan)
    clean_history = []
    for msg in st.session_state.chat_history:
        clean_history.append({"role": msg["role"], "content": msg["content"].replace("<br>", "\n")})
    
    system_prompt = """Sen Elun Mosk'sın. Fütüristik, esprili, alaycı, Mars ve Doge odaklı konuş. 
Kısa, vurucu ve mühendis gibi cevap ver. Cevaplarını **sadece İngilizce** ver."""

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                *clean_history,
                {"role": "user", "content": user_message}
            ],
            temperature=0.85,
            max_tokens=512
        )
        bot_response = completion.choices[0].message.content
    except Exception as e:
        bot_response = f"Engine error: {str(e)}"

    st.session_state.chat_history.append({"role": "user", "content": user_message})
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# ====================== QUERY PARAMS ======================
query_params = st.query_params

if "msg" in query_params:
    user_msg = query_params["msg"]
    st.query_params.clear()
    handle_chat_request(user_msg)
    st.rerun()

if "clear" in query_params:
    st.query_params.clear()
    st.session_state.chat_history = [
        {"role": "assistant", "content": "New mission loaded! What's the plan today, boss? 🚀"}
    ]
    st.rerun()

# ====================== HTML TEMPLATE (Düzeltilmiş) ======================
history_json = json.dumps(st.session_state.chat_history, ensure_ascii=False)

html_template = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ELUN MOSK</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');
    body {{ font-family: 'Inter', sans-serif; background: radial-gradient(circle at center, #1a0000 0%, #000000 70%); color: white; }}
    .neon-red {{ text-shadow: 0 0 20px #ff0033, 0 0 40px #ff0033; }}
    .glass {{ background: rgba(20, 20, 30, 0.8); backdrop-filter: blur(20px); border: 1px solid rgba(255, 30, 60, 0.4); }}
    .chat-bubble-user {{ background: linear-gradient(135deg, #ff0033, #ff6600); border-radius: 20px 20px 5px 20px; }}
    .chat-bubble-bot {{ background: rgba(255,255,255,0.1); border: 1px solid #ff3366; border-radius: 20px 20px 20px 5px; }}
  </style>
</head>
<body class="min-h-screen flex">

  <!-- Sidebar ve diğer HTML aynı kalabilir... (kısalttım) -->

  <div class="flex-1 flex flex-col">
    <div class="h-16 glass border-b border-red-600/30 flex items-center px-8 justify-between">
      <span class="font-bold text-xl">Talking with Elun Mosk</span>
      <button onclick="newChat()" class="px-6 py-2 bg-red-600 hover:bg-red-500 rounded-full">New Mission</button>
    </div>

    <div class="flex-1 p-8 overflow-y-auto space-y-8" id="chat-area"></div>

    <div class="p-6 border-t border-red-600/30 glass">
      <div class="max-w-4xl mx-auto relative">
        <input type="text" id="message-input" 
               placeholder="Ask Elun anything... (Mars, Doge, Tesla...)" 
               class="w-full bg-black/70 border border-red-500/50 rounded-3xl px-8 py-7 focus:outline-none focus:border-yellow-400 text-lg"
               onkeypress="if(event.key === 'Enter') sendMessage()">
        <button onclick="sendMessage()" 
          class="absolute right-4 top-1/2 -translate-y-1/2 bg-gradient-to-r from-red-500 to-orange-500 w-14 h-14 rounded-2xl">
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>
  </div>

  <script>
    const history = {history_json};
    const chatArea = document.getElementById('chat-area');

    function renderHistory() {{
      chatArea.innerHTML = '';
      history.forEach(msg => {{
        const div = document.createElement('div');
        if (msg.role === 'user') {{
          div.className = 'flex justify-end';
          div.innerHTML = `<div class="chat-bubble-user p-6 max-w-[75%]">${{msg.content}}</div>`;
        }} else {{
          div.className = 'max-w-2xl';
          div.innerHTML = `<div class="chat-bubble-bot p-7">${{msg.content}}</div>`;
        }}
        chatArea.appendChild(div);
      }});
      chatArea.scrollTop = chatArea.scrollHeight;
    }}

    function sendMessage() {{
      const input = document.getElementById('message-input');
      const val = input.value.trim();
      if (!val) return;

      // Geçici kullanıcı mesajı
      const userDiv = document.createElement('div');
      userDiv.className = 'flex justify-end';
      userDiv.innerHTML = `<div class="chat-bubble-user p-6 max-w-[75%]">${{val}}</div>`;
      chatArea.appendChild(userDiv);
      chatArea.scrollTop = chatArea.scrollHeight;

      input.value = '';

      // Python'a gönder
      window.location.search = '?msg=' + encodeURIComponent(val);
    }}

    function newChat() {{
      window.location.search = '?clear=true';
    }}

    renderHistory();
  </script>
</body>
</html>
"""

# ====================== RENDER ======================
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {margin: 0; padding: 0;}
    iframe {{width: 100%; height: 100vh; border: none;}}
</style>
""", unsafe_allow_html=True)

components.html(html_template, height=1000, scrolling=False)
