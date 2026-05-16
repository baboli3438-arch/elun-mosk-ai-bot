import streamlit as st
import json
from groq import Groq
import streamlit.components.v1 as components

# ====================== API ======================
groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY bulunamadı!")
    st.stop()

client = Groq(api_key=groq_api_key)

# ====================== SESSION STATE ======================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Yo, what's up? 🚀<br><br>I'm <b>Elun Mosk</b>.<br>Ready to talk about Mars, Doge, Tesla, and memes?"}
    ]

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# ====================== CHAT HANDLER ======================
def send_message():
    if st.session_state.user_input and st.session_state.user_input.strip():
        user_msg = st.session_state.user_input.strip()
        
        # Kullanıcı mesajını ekle
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        
        # System Prompt
        system_prompt = """
        Sen Elun Mosk'sın. Fütüristik, esprili, alaycı ve vizyoner konuş. 
        Kısa, vurucu cevaplar ver. İngilizce cevap ver.
        """
        
        try:
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.chat_history
                ],
                temperature=0.85,
                max_tokens=600
            )
            response = completion.choices[0].message.content
        except Exception as e:
            response = f"⚠️ Mission error: {str(e)}"
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.session_state.user_input = ""  # Input'u temizle
        st.session_state.input_key += 1   # Input alanını resetle

# ====================== HTML TEMPLATE ======================
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
    
    body {{
      font-family: 'Inter', sans-serif;
      background: radial-gradient(circle at center, #1a0000 0%, #000000 70%);
      color: white;
      margin: 0;
      height: 100vh;
      overflow: hidden;
    }}
    .neon-red {{ text-shadow: 0 0 20px #ff0033, 0 0 40px #ff0033; }}
    .glass {{ background: rgba(20,20,30,0.85); backdrop-filter: blur(20px); border: 1px solid rgba(255,50,80,0.4); }}
    .chat-bubble-user {{ background: linear-gradient(135deg, #ff0033, #ff6600); border-radius: 20px 20px 5px 20px; }}
    .chat-bubble-bot {{ background: rgba(255,255,255,0.1); border: 1px solid #ff3366; border-radius: 20px 20px 20px 5px; }}
  </style>
</head>
<body class="flex">

  <!-- Sidebar -->
  <div class="w-80 glass border-r border-red-600/40 p-6 flex flex-col">
    <div class="flex items-center gap-4 mb-10">
      <div class="w-20 h-20 bg-gradient-to-br from-red-500 to-orange-500 rounded-3xl flex items-center justify-center text-5xl shadow-2xl">🚀</div>
      <div>
        <h1 class="text-4xl font-bold tracking-widest neon-red">ELUN MOSK</h1>
        <p class="text-red-400 text-sm">ONLINE • MEME MODE</p>
      </div>
    </div>
    <div class="mt-auto text-xs text-gray-500 text-center">xAI • Tesla • SpaceX • 2026</div>
  </div>

  <!-- Main Chat Area -->
  <div class="flex-1 flex flex-col">
    <div class="h-16 glass border-b border-red-600/30 flex items-center px-8">
      <span class="font-bold text-xl">Talking with Elun Mosk</span>
    </div>

    <div class="flex-1 p-8 overflow-y-auto space-y-6" id="chat-area"></div>

    <div class="p-6 glass border-t border-red-600/30">
      <form id="chat-form">
        <div class="max-w-4xl mx-auto relative">
          <input type="text" id="user-input" 
                 placeholder="Ask Elun anything... (Mars, Doge, Tesla, xAI)" 
                 class="w-full bg-black/70 border border-red-500/50 rounded-3xl px-8 py-7 focus:outline-none focus:border-yellow-400 text-lg">
          <button type="submit" 
            class="absolute right-4 top-1/2 -translate-y-1/2 bg-gradient-to-r from-red-500 to-orange-500 w-14 h-14 rounded-2xl flex items-center justify-center hover:scale-110 transition">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </form>
    </div>
  </div>

  <script>
    const history = {history_json};
    const chatArea = document.getElementById('chat-area');

    function renderChat() {{
      chatArea.innerHTML = '';
      history.forEach(msg => {{
        const div = document.createElement('div');
        if (msg.role === 'user') {{
          div.className = 'flex justify-end';
          div.innerHTML = `<div class="chat-bubble-user p-6 max-w-[70%] text-white">${{msg.content}}</div>`;
        }} else {{
          div.className = 'max-w-2xl';
          div.innerHTML = `<div class="chat-bubble-bot p-7">${{msg.content}}</div>`;
        }}
        chatArea.appendChild(div);
      }});
      chatArea.scrollTop = chatArea.scrollHeight;
    }}

    // Form submit
    document.getElementById('chat-form').addEventListener('submit', function(e) {{
      e.preventDefault();
      const input = document.getElementById('user-input');
      const message = input.value.trim();
      
      if (message === '') return;

      // Python'a mesajı gönder (Streamlit widget üzerinden)
      window.parent.postMessage({{type: 'streamlit:setComponentValue', value: message}}, '*');
      
      input.value = '';
    }});

    renderChat();
  </script>
</body>
</html>
"""

# ====================== STREAMLIT UI ======================
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {margin:0; padding:0;}
    iframe {width:100%; height:100vh; border:none;}
</style>
""", unsafe_allow_html=True)

# Mesaj gönderme inputu (gizli)
user_message = st.text_input("Message", key=f"input_{st.session_state.input_key}", label_visibility="collapsed")

if user_message:
    st.session_state.user_input = user_message
    send_message()
    st.rerun()

# HTML'i render et
components.html(html_template, height=900, scrolling=False)
