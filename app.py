import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# ======================================================
# CONFIG
# ======================================================
st.set_page_config(
    page_title="ELUN MOSK",
    layout="wide"
)

# ======================================================
# API
# ======================================================
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ======================================================
# CSS
# ======================================================
st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at center,#1a0000 0%,#000000 70%);
    color:white;
}

#MainMenu,
footer,
header{
    visibility:hidden;
}

.user-msg{
    background:linear-gradient(135deg,#ff0033,#ff6600);
    padding:18px;
    border-radius:20px 20px 5px 20px;
    margin:10px 0;
    width:fit-content;
    margin-left:auto;
    max-width:70%;
    color:white;
    font-weight:600;
}

.bot-msg{
    background:rgba(255,255,255,0.07);
    border:1px solid #ff3366;
    padding:18px;
    border-radius:20px 20px 20px 5px;
    margin:10px 0;
    width:fit-content;
    max-width:70%;
    color:white;
}

.title{
    color:white;
    font-size:48px;
    font-weight:800;
    text-shadow:
    0 0 10px #ff0033,
    0 0 20px #ff0033;
}

.sidebar-btn{
    width:100%;
    padding:18px;
    border-radius:18px;
    background:#111122;
    border:1px solid #ff0033;
    color:white;
    margin-bottom:10px;
    cursor:pointer;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Yo, what's up? 🚀"
        }
    ]

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:

    st.markdown(
        "<div class='title'>ELUN<br>MOSK</div>",
        unsafe_allow_html=True
    )

    st.write("🟢 ONLINE • MEME MODE")

    if st.button("🚀 Mars Mission"):
        prompt = "When are we going to Mars?"
        st.session_state.prompt = prompt

    if st.button("🐕 Dogecoin"):
        prompt = "Will Dogecoin reach 1 dollar?"
        st.session_state.prompt = prompt

    if st.button("🤖 Tesla AI"):
        prompt = "Tell me about Tesla AI."
        st.session_state.prompt = prompt

# ======================================================
# TITLE
# ======================================================
st.markdown("# 🤖 Talking with Elun Mosk")

# ======================================================
# CHAT RENDER
# ======================================================
for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div class='user-msg'>
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class='bot-msg'>
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# ======================================================
# CHAT INPUT
# ======================================================
prompt = st.chat_input("Ask Elun anything...")

if "prompt" in st.session_state:
    prompt = st.session_state.prompt
    del st.session_state.prompt

# ======================================================
# AI RESPONSE
# ======================================================
if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    st.rerun()

# ======================================================
# GENERATE RESPONSE
# ======================================================
last_msg = st.session_state.messages[-1]

if last_msg["role"] == "user":

    with st.spinner("Analyzing rockets... 🚀"):

        try:

            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role":"system",
                        "content":"""
                        You are Elun Mosk.
                        Speak futuristic.
                        Love Mars.
                        Love Dogecoin.
                        Be funny.
                        Use meme culture.
                        Keep responses short.
                        """
                    },
                    *st.session_state.messages
                ],
                temperature=0.9,
                max_tokens=300
            )

            answer = completion.choices[0].message.content

        except Exception as e:

            answer = f"🚨 Mission Failure: {str(e)}"

    st.session_state.messages.append({
        "role":"assistant",
        "content":answer
    })

    st.rerun()
