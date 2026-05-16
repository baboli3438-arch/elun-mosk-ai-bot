import streamlit as st
import os
import json
from groq import Groq
from dotenv import load_dotenv
import streamlit.components.v1 as components

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="ELUN MOSK",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# API
# =====================================================================
load_dotenv()

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("🚨 GROQ API KEY NOT FOUND")
    st.stop()

client = Groq(api_key=groq_api_key)

# =====================================================================
# SESSION
# =====================================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": """
            Yo, what's up? 🚀<br><br>

            I'm <span class='text-red-400 font-bold'>Elun Mosk</span>.<br>

            Ready to talk about Mars, Doge, Tesla and memes?<br><br>

            What's your command, boss?
            """
        }
    ]

# =====================================================================
# AI FUNCTION
# =====================================================================
def handle_chat_request(user_message):

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_message
    })

    system_prompt = """
    Sen Elun Mosk'sın.
    Mars fanatiği ol.
    Dogecoin sev.
    Tesla ve SpaceX hakkında konuş.
    Hafif alaycı ol.
    Meme kültürü kullan.
    İngilizce konuş.
    Cevapları kısa ve havalı ver.
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
        🚨 Mission Failure<br><br>
        {str(e)}
        """

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_response
    })

# =====================================================================
# URL PARAMS
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
            🚀 New Mission Loaded.<br><br>
            What's the plan today, boss?
            """
        }
    ]

    st.rerun()

# =====================================================================
# CHAT HISTORY JSON
# =====================================================================
history_json = json.dumps(st.session_state.chat_history)

# =====================================================================
# HTML
# =====================================================================
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
    height: 100vh;
    font-family: 'Inter', sans-serif;
    background:
    radial-gradient(circle at center, #1a0000 0%, #000000 70%);
    color: white;
}}

.glass {{
    background: rgba(20,20,30,0.75);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,30,60,0.35);
}}

.neon-red {{
    text-shadow:
    0 0 10px #ff0033,
    0 0 20px #ff0033,
    0 0 40px #ff0033;
}}

.chat-user {{
    background:
    linear-gradient(135deg,#ff0033,#ff6600);
    border-radius: 20px 20px 5px 20px;
}}

.chat-bot {{
    background: rgba(255,255,255,0.07);
    border: 1px solid #ff3366;
    border-radius: 20px 20px 20px 5px;
}}

.scanline::after {{
    content: '';
    position: absolute;
    width: 100%;
    height: 4px;
    top: -50%;
    left: 0;
    background:
    linear-gradient(transparent,#ff0033,transparent);
    animation: scan 5s linear infinite;
    opacity: 0.25;
}}

@keyframes scan {{
    0% {{ top: -50%; }}
    100% {{ top: 200%; }}
}}

</style>

</head>

<body class="flex">

<!-- LEFT -->
<div class="w-80 glass border-r border-red-500/30 p-6 flex flex-col">

    <div class="flex items-center gap-4 mb-10">

        <div class="w-20 h-20 rounded-3xl bg-gradient-to-br from-red-500 via-orange-500 to-yellow-400 flex items-center justify-center text-5xl border-4 border-yellow-300 shadow-2xl">
            🚀
        </div>

        <div>
            <h1 class="text-4xl font-bold neon-red tracking-widest">
                ELUN MOSK
            </h1>

            <p class="text-red-400 text-sm flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
                ONLINE • MEME MODE
            </p>
        </div>

    </div>

    <div class="space-y-4">

        <button onclick="quickReply('When are we going to Mars?')"
        class="glass p-5 rounded-2xl hover:border-yellow-400 transition w-full text-left">

            🚀 Mars Mission

        </button>

        <button onclick="quickReply('Will Dogecoin reach 1 dollar?')"
        class="glass p-5 rounded-2xl hover:border-yellow-400 transition w-full text-left">

            🐕 Dogecoin

        </button>

        <button onclick="quickReply('Tell me about Tesla AI.')"
        class="glass p-5 rounded-2xl hover:border-yellow-400 transition w-full text-left">

            🤖 Tesla AI

        </button>

    </div>

    <div class="mt-auto text-xs text-center text-gray-500">
        xAI • Tesla • SpaceX • 2026
    </div>

</div>

<!-- MAIN -->
<div class="flex-1 flex flex-col scanline relative">

    <!-- TOPBAR -->
    <div class="h-16 glass border-b border-red-500/30 flex items-center justify-between px-8">

        <div class="flex items-center gap-3">

            <i class="fas fa-robot text-red-500 text-2xl"></i>

            <span class="font-bold text-xl">
                Talking with Elun Mosk
            </span>

        </div>

        <button onclick="newChat()"
        class="px-6 py-2 bg-red-600 hover:bg-red-500 rounded-full">

            New Mission

        </button>

    </div>

    <!-- CHAT -->
    <div id="chat-area"
    class="flex-1 overflow-y-auto p-8 space-y-6">
    </div>

    <!-- INPUT -->
    <div class="p-6 glass border-t border-red-500/30">

        <div class="max-w-4xl mx-auto relative">

            <input
            type="text"
            id="message-input"
            placeholder="Ask Elun anything..."
            class="w-full bg-black/70 border border-red-500/40 rounded-3xl px-8 py-6 text-lg focus:outline-none focus:border-yellow-400"
            onkeypress="if(event.key === 'Enter') sendMessage()"
            >

            <button
            onclick="sendMessage()"
            class="absolute right-4 top-1/2 -translate-y-1/2 w-14 h-14 rounded-2xl bg-gradient-to-r from-red-500 to-orange-500 hover:scale-110 transition">

                <i class="fas fa-paper-plane text-xl"></i>

            </button>

        </div>

    </div>

</div>

<script>

const history = {history_json};

const chatArea = document.getElementById('chat-area');

function renderHistory() {{

    const oldLoading = document.getElementById('loading-message');

    if(oldLoading) {{
        oldLoading.remove();
    }}

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

    const loading = document.createElement('div');

    loading.className = 'max-w-2xl';

    loading.id = 'loading-message';

    loading.innerHTML = `
    <div class="chat-bot p-7 inline-block animate-pulse">
        Analyzing rockets... 🚀
    </div>
    `;

    chatArea.appendChild(loading);

    chatArea.scrollTop = chatArea.scrollHeight;

    input.value = '';

    window.parent.postMessage(
        {{
            type: "streamlit:setQueryParams",
            params: {{
                msg: val
            }}
        }},
        "*"
    );

}}

function quickReply(text) {{

    document.getElementById('message-input').value = text;

    sendMessage();

}}

function newChat() {{

    window.parent.postMessage(
        {{
            type: "streamlit:setQueryParams",
            params: {{
                clear: "true"
            }}
        }},
        "*"
    );

}}

</script>

</body>
</html>
"""

# =====================================================================
# HIDE STREAMLIT
# =====================================================================
st.markdown(
    """
    <style>

    #MainMenu {
        visibility:hidden;
    }

    header {
        visibility:hidden;
    }

    footer {
        visibility:hidden;
    }

    .stApp {
        margin:0;
        padding:0;
    }

    iframe {
        position:fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        border:none;
        z-index:999999;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# RENDER
# =====================================================================
components.html(
    html_template,
    height=1080,
    scrolling=True
)
