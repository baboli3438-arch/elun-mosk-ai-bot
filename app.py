<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ELUN MOSK • To Mars?</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');
    
    body {
      font-family: 'Inter', sans-serif;
      background: radial-gradient(circle at center, #1a0000 0%, #000000 70%);
      color: white;
      overflow: hidden;
    }
    
    .neon-red { 
      text-shadow: 0 0 20px #ff0033, 0 0 40px #ff0033; 
    }
    
    .glass { 
      background: rgba(20, 20, 30, 0.75);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 30, 60, 0.35);
    }
    
    .chat-bubble-user {
      background: linear-gradient(135deg, #ff0033, #ff6600);
      border-radius: 20px 20px 5px 20px;
    }
    
    .chat-bubble-bot {
      background: rgba(255,255,255,0.09);
      border: 1px solid #ff3366;
      border-radius: 20px 20px 20px 5px;
    }
    
    .scanline::after {
      content: '';
      position: absolute;
      top: -50%;
      left: 0;
      width: 100%;
      height: 4px;
      background: linear-gradient(transparent, #ff0033, transparent);
      animation: scan 4.5s linear infinite;
      opacity: 0.25;
    }
    
    @keyframes scan { 0% { top: -50%; } 100% { top: 200%; } }
  </style>
</head>
<body class="min-h-screen flex">

  <!-- Sidebar -->
  <div class="w-80 glass border-r border-red-600/40 p-6 flex flex-col">
    <div class="flex items-center gap-4 mb-10">
      <div class="w-20 h-20 bg-gradient-to-br from-red-500 via-orange-500 to-yellow-400 rounded-3xl flex items-center justify-center text-5xl shadow-2xl shadow-red-600/70 border-4 border-yellow-300">
        🚀
      </div>
      <div>
        <h1 class="text-4xl font-bold tracking-widest neon-red">ELUN MOSK</h1>
        <p class="text-red-400 flex items-center gap-2 text-sm">
          <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          ONLINE • MEME MODE
        </p>
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
          <button class="p-5 rounded-2xl glass border border-red-500 text-left hover:scale-105 transition">
            <i class="fas fa-rocket text-red-400"></i>
            <p class="font-medium mt-1">Mars Mode</p>
          </button>
          <button class="p-5 rounded-2xl glass hover:border-yellow-400 transition text-left">
            <i class="fas fa-dog text-yellow-400"></i>
            <p class="font-medium mt-1">Doge Mode</p>
          </button>
        </div>
      </div>
    </div>

    <div class="mt-auto text-center text-xs text-gray-500">
      xAI • Tesla • SpaceX • 2026
    </div>
  </div>

  <!-- Main Chat Area -->
  <div class="flex-1 flex flex-col scanline">
    <div class="h-16 glass border-b border-red-600/30 flex items-center px-8 justify-between">
      <div class="flex items-center gap-3">
        <i class="fas fa-robot text-red-500 text-2xl"></i>
        <span class="font-bold text-xl">Talking with Elun Mosk</span>
      </div>
      <div class="flex items-center gap-6 text-sm">
        <button class="flex items-center gap-2 hover:text-cyan-400 transition">
          <i class="fas fa-microphone"></i>
          <span>Voice Mode</span>
        </button>
        <button onclick="newChat()" class="px-6 py-2.5 bg-red-600 hover:bg-red-500 rounded-full font-medium transition">
          New Mission
        </button>
      </div>
    </div>

    <!-- Messages -->
    <div class="flex-1 p-8 overflow-y-auto space-y-8" id="chat-area">
      <div class="max-w-2xl">
        <div class="chat-bubble-bot p-7 inline-block">
          Yo Yellow! 🚀<br><br>
          I'm <span class="text-red-400 font-bold">Elun Mosk</span>.<br>
          Ready to talk about Mars, Doge, Tesla, and memes?<br>
          What's your command, boss?
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="p-6 border-t border-red-600/30 glass">
      <div class="max-w-4xl mx-auto relative">
        <input 
          type="text" 
          id="message-input"
          placeholder="Ask Elun anything... (Mars, Doge, Tesla, xAI...)" 
          class="w-full bg-black/70 border border-red-500/50 rounded-3xl px-8 py-7 focus:outline-none focus:border-yellow-400 text-lg placeholder-gray-400"
          onkeypress="if(event.key === 'Enter') sendMessage()">
        <button onclick="sendMessage()" 
          class="absolute right-4 top-1/2 -translate-y-1/2 bg-gradient-to-r from-red-500 to-orange-500 w-14 h-14 rounded-2xl flex items-center justify-center hover:scale-110 transition">
          <i class="fas fa-paper-plane text-xl"></i>
        </button>
      </div>
      <p class="text-center text-[10px] text-gray-500 mt-4 tracking-widest">ELUN MOSK v69 • MEME NEURAL NETWORK • 2026</p>
    </div>
  </div>

  <!-- Right Panel -->
  <div class="w-72 glass border-l border-red-600/30 p-6 hidden lg:block">
    <h3 class="uppercase text-xs tracking-widest mb-6 text-red-400">QUICK MISSIONS</h3>
    <div class="space-y-3">
      <div onclick="quickReply('When are we going to Mars?')" class="glass p-4 rounded-2xl hover:border-yellow-400 cursor-pointer transition">🚀 When are we going to Mars?</div>
      <div onclick="quickReply('Will Dogecoin reach $1?')" class="glass p-4 rounded-2xl hover:border-yellow-400 cursor-pointer transition">🐕 Will Dogecoin reach $1?</div>
      <div onclick="quickReply('Should I buy Tesla stock?')" class="glass p-4 rounded-2xl hover:border-yellow-400 cursor-pointer transition">📈 Should I buy Tesla stock?</div>
    </div>
  </div>
</body>

<script>
function sendMessage() {
  const input = document.getElementById('message-input');
  const chatArea = document.getElementById('chat-area');
  
  if (input.value.trim() === '') return;

  const userMsg = document.createElement('div');
  userMsg.className = 'flex justify-end';
  userMsg.innerHTML = `
    <div class="chat-bubble-user p-6 max-w-[75%]">
      ${input.value}
    </div>
  `;
  chatArea.appendChild(userMsg);
  chatArea.scrollTop = chatArea.scrollHeight;

  const question = input.value.toLowerCase();
  input.value = '';

  setTimeout(() => {
    let reply = "Haha, great question! 🔥";

    if (question.includes("mars")) {
      reply = "We're sending humans in 2026. You coming or what? 🪐";
    } else if (question.includes("doge") || question.includes("dogecoin")) {
      reply = "TO THE MOON!!! 🐕🚀 $1 is inevitable.";
    } else if (question.includes("tesla")) {
      reply = "Buy Tesla. Also buy Cybertruck. Maximum meme energy.";
    } else if (question.includes("xai") || question.includes("groq") || question.includes("grok")) {
      reply = "xAI will save the world. Grok is trying to be smarter than me 😂";
    }

    const botMsg = document.createElement('div');
    botMsg.className = 'max-w-2xl';
    botMsg.innerHTML = `
      <div class="chat-bubble-bot p-7 inline-block">
        ${reply}
      </div>
    `;
    chatArea.appendChild(botMsg);
    chatArea.scrollTop = chatArea.scrollHeight;
  }, 700);
}

function quickReply(text) {
  document.getElementById('message-input').value = text;
  sendMessage();
}

function newChat() {
  if (confirm("Start a new mission?")) {
    document.getElementById('chat-area').innerHTML = `
      <div class="max-w-2xl">
        <div class="chat-bubble-bot p-7 inline-block">
          New mission loaded!<br><br>
          What's the plan today, boss? 🚀
        </div>
      </div>`;
  }
}
</script>
</html>
