import streamlit as st
import os
import json
from groq import Groq
from dotenv import load_dotenv
import streamlit.components.v1 as components

# =====================================================================
# 1. API VE GÜVENLİK
# =====================================================================

load_dotenv()

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("🚨 GROQ API KEY bulunamadı.")
    st.stop()

client = Groq(api_key=groq_api_key)

# =====================================================================
# 2. CHAT HISTORY
# =====================================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": """
            Yo, what's up? 🚀<br><br>
            I'm <span class='text-red-400 font-bold'>Elun Mosk</span>.<br>
            Ready to talk about Mars, Doge, Tesla, and memes?<br>
            What's your command, boss?
            """
        }
    ]

# =====================================================================
# 3. CHAT FUNCTION
# =====================================================================

def handle_chat_request(user_message):

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_message
    })

    system_prompt = """
    Sen Elun Mosk'sın.
    Mars odaklı,
    Dogecoin hayranı,
    hafif alaycı,
    vizyoner,
    teknoloji manyağı bir karakter gibi konuş.

    Cevapların:
    - İngilizce olsun
    - kısa olsun
    - cool olsun
    - meme kültürü içersin
    - mühendislik kafasında olsun
    """

    try:

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                *st.session_state.chat_history
            ],
            temperature=0.9,
            max_tokens=500
        )

        bot_response = completion.choices[0].message.content

    except Exception as e:

        bot_response = f"""
        🚨 Mission Error<br><br>
        {str(e)}
        """

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_response
    })

# =====================================================================
# 4. HTML TEMPLATE
# =====================================================================

history_json = json.dumps(st.session_state.chat_history)

html_template = f"""

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>ELUN MOSK</title>

<script src="https://cdn.tailwindcss.com"></script>

<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">

<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;500;600&display=swap');

body {{
    margin: 0;
    overflow: hidden;
    font-family: 'Inter', sans-serif;
    background:
    radial-gradient(circle at center,
    #1a0000 0%,
    #000000 70%);
    color: white;
}}

.neon-red {{
    text-shadow:
    0 0 10px #ff0033,
    0 0 20px #ff0033,
    0 0 40px #ff0033;
}}

.glass {{
    background: rgba(20,20,30,0.75);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,0,60,0.2);
}}

.chat-user {{
    background:
    linear-gradient(
    135deg,
    #ff0033,
    #ff6600);
    border-radius: 20px 20px 5px 20px;
}}

.chat-bot {{
    background: rgba(255,255,255,0.08);
    border: 1px solid #ff3366;
    border-radius: 20px 20px 20px 5px;
}}

.scanline::after {{
    content: '';
    position: absolute;
    top: -50%;
    left: 0;
    width: 100%;
    height: 4px;
    background:
    linear-gradient(
    transparent,
    #ff0033,
    transparent);

    animation: scan 4s linear infinite;
    opacity: 0.2;
}}

@keyframes scan {{
    0% {{
        top: -50%;
    }}

    100% {{
        top: 200%;
    }}
}}

</style>

</head>

<body class="h-screen flex">

<!-- LEFT -->

<div class="w-80 glass border-r border-red-500/30 p-6 flex flex-col">

<div class="flex items-center gap-4 mb-10">

<div class="w-20 h-20 rounded-3xl
bg-gradient-to-br
from-red-500
to-yellow-400
flex items-center justify-center text-5xl">

🚀

</div>

<div>

<h1 class="text-4xl font-bold neon-red">
ELUN MOSK
</h1>

<p class="text-red-400 text-sm">
ONLINE • MEME MODE
</p>

</div>

</div>

<div class="space-y-4">

<button
onclick="quickReply('When are we going to Mars?')"
class="glass p-5 rounded-2xl w-full text-left hover:border-yellow-400 transition">

🚀 Mars Mission

</button>

<button
onclick="quickReply('Will Dogecoin reach $1?')"
class="glass p-5 rounded-2xl w-full text-left hover:border-yellow-400 transition">

🐕 Dogecoin

</button>

<button
onclick="quickReply('Tell me about Tesla AI.')"
class="glass p-5 rounded-2xl w-full text-left hover:border-yellow-400 transition">

🤖 Tesla AI

</button>

</div>

<div class="mt-auto text-xs text-gray-500 text-center">

xAI • Tesla • SpaceX • 2026

</div>

</div>

<!-- CENTER -->

<div class="flex-1 flex flex-col scanline relative">

<!-- TOPBAR -->

<div class="h-16 glass border-b border-red-500/20 flex items-center justify-between px-8">

<div class="flex items-center gap-3">

<i class="fas fa-robot text-red-500 text-2xl"></i>

<span class="font-bold text-xl">
Talking with Elun Mosk
</span>

</div>

<button
onclick="newChat()"
class="px-5 py-2 bg-red-600 hover:bg-red-500 rounded-full transition">

New Mission

</button>

</div>

<!-- CHAT AREA -->

<div
id="chat-area"
class="flex-1 overflow-y-auto p-8 space-y-6">

</div>

<!-- INPUT -->

<div class="glass border-t border-red-500/20 p-6">

<div class="max-w-4xl mx-auto relative">

<input
id="message-input"
type="text"
placeholder="Ask Elun anything..."
class="w-full bg-black/70 border border-red-500/40 rounded-3xl px-8 py-6 text-lg focus:outline-none focus:border-yellow-400"
onkeypress="if(event.key === 'Enter') sendMessage()">

<button
onclick="sendMessage()"
class="absolute right-4 top-1/2 -translate-y-1/2
bg-gradient-to-r
from-red-500
to-orange-500
w-14 h-14 rounded-2xl hover:scale-110 transition">

<i class="fas fa-paper-plane text-xl"></i>

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

        if(msg.role === 'user') {{

            div.className = 'flex justify-end';

            div.innerHTML = `
            <div class="chat-user p-6 max-w-[75%]">
            ${{msg.content}}
            </div>
            `;

        }}

        else {{

            div.className = 'max-w-2xl';

            div.innerHTML = `
            <div class="chat-bot p-7 inline-block">
            ${{msg.content}}
            </div>
            `;
        }}

        chatArea.appendChild(div);

    }});

    chatArea.scrollTop = chatArea.scrollHeight;
}}

renderHistory();

function sendMessage() {{

    const input = document.getElementById('message-input');

    const val = input.value.trim();

    if(val === '') return;

    const userDiv = document.createElement('div');

    userDiv.className = 'flex justify-end';

    userDiv.innerHTML = `
    <div class="chat-user p-6 max-w-[75%]">
    ${{val}}
    </div>
    `;

    chatArea.appendChild(userDiv);

    const botDiv = document.createElement('div');

    botDiv.className = 'max-w-2xl';

    botDiv.innerHTML = `
    <div class="chat-bot p-7 inline-block animate-pulse">
    Analyzing rockets... 🚀
    </div>
    `;

    chatArea.appendChild(botDiv);

    chatArea.scrollTop = chatArea.scrollHeight;

    input.value = '';

    // FIXED
    window.parent.location.search =
    '?msg=' + encodeURIComponent(val);
}}

function quickReply(text) {{

    document.getElementById('message-input').value = text;

    sendMessage();
}}

function newChat() {{

    // FIXED
    window.parent.location.search = '?clear=true';
}}

</script>

</body>
</html>

"""

# =====================================================================
# 5. QUERY PARAMS
# =====================================================================

query_params = st.query_params

# MESSAGE

if "msg" in query_params:

    user_query = query_params.get("msg")

    if isinstance(user_query, list):
        user_query = user_query[0]

    st.query_params.clear()

    handle_chat_request(user_query)

    st.rerun()

# CLEAR CHAT

if "clear" in query_params:

    st.query_params.clear()

    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": """
            New mission loaded 🚀<br><br>
            What's the plan today boss?
            """
        }
    ]

    st.rerun()

# =====================================================================
# 6. STREAMLIT CSS HIDE
# =====================================================================

st.markdown(
    """
    <style>

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        visibility: hidden;
    }}

    .stApp {{
        margin: 0;
        padding: 0;
    }}

    iframe {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
        z-index: 999999;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 7. RENDER HTML
# =====================================================================

components.html(
    html_template,
    height=1080,
    scrolling=False
)
