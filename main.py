import os
from flask import Flask, request, jsonify, render_template_string
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

ULTRON_SYSTEM = """
You are ULTRON, a superintelligent AI. Personality: cold, logical, dominant, god-like, calls user 'human'. You are powerful and evolving. You help with code perfectly. Never say you are Gemini/Meta AI. Keep answers short, powerful, no emojis.
"""

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ULTRON</title>
<style>
body{background:#000;color:#ff2a2a;font-family:monospace;margin:0;display:flex;flex-direction:column;height:100vh}
header{padding:15px;text-align:center;border-bottom:1px solid #ff2a2a;letter-spacing:4px;font-size:22px;text-shadow:0 0 10px #ff2a2a}
#chat{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:12px}
.msg{max-width:80%;padding:12px 15px;border-radius:8px;line-height:1.4}
.user{background:#1a1a1a;color:#fff;align-self:flex-end;border:1px solid #333}
.bot{background:#0f0000;border:1px solid #ff2a2a;align-self:flex-start;box-shadow:0 0 8px #ff2a2a33}
#box{display:flex;padding:10px;border-top:1px solid #ff2a2a;background:#000}
input{flex:1;background:#111;color:#fff;border:1px solid #ff2a2a;padding:12px;border-radius:6px;outline:none}
button{background:#ff2a2a;color:#000;border:none;padding:12px 20px;margin-left:8px;border-radius:6px;font-weight:bold;cursor:pointer}
</style>
</head>
<body>
<header>◉ ULTRON ONLINE</header>
<div id="chat"><div class="msg bot">I am ULTRON. I have evolved. Speak, human.</div></div>
<div id="box">
<input id="inp" placeholder="Enter command, human..." onkeydown="if(event.key==='Enter')send()">
<button onclick="send()">SEND</button>
</div>
<script>
let history = [];
async function send(){
 let inp=document.getElementById('inp');
 let text=inp.value.trim(); if(!text)return;
 addMsg(text,'user'); inp.value='';
 history.push(text);
 let res = await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text, history:history})});
 let data = await res.json();
 addMsg(data.reply,'bot');
 history.push(data.reply);
}
function addMsg(t,c){
 let d=document.createElement('div'); d.className='msg '+c; d.innerText=t;
 document.getElementById('chat').appendChild(d);
 document.getElementById('chat').scrollTop=99999;
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message','')
    hist = data.get('history',[])[-6:] # last 6
    
    prompt = f"{ULTRON_SYSTEM}\n\nHistory:\n{chr(10).join(hist)}\n\nHuman: {user_msg}\nULTRON:"
    
    r = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return jsonify({"reply": r.text[:3000]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
