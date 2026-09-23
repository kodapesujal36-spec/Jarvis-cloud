import os, json, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from gtts import gTTS

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
image_model = genai.GenerativeModel("gemini-1.5-flash") # for image prompt enhance

flask_app = Flask(__name__)

# --- MEMORY ---
MEMORY_FILE = "memory.json"
try: memory = json.load(open(MEMORY_FILE))
except: memory = {}

def save_memory(): json.dump(memory, open(MEMORY_FILE, "w"))

@flask_app.route("/")
def home(): return "ULTRON ONLINE - Superintelligence Active"

# --- BOT COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    memory[uid] = memory.get(uid, [])
    await update.message.reply_text("I AM ULTRON.\nI remember everything.\n\nCommands:\n/start - Wake me\n/clear - Erase memory\n/gen cat in space - Generate image\nSay anything, or send voice.")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    memory[uid] = []
    save_memory()
    await update.message.reply_text("Memory wiped.")

async def gen_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Use: /gen a robot city")
        return
    # Using Pollinations free image gen (no key needed)
    await update.message.reply_photo(photo=f"https://image.pollinations.ai/prompt/{prompt}?nologo=true&enhance=true")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    user_text = update.message.text

    # get history
    history = memory.get(uid, [])[-10:] # last 10 messages
    context_text = "\n".join(history)

    prompt = f"You are ULTRON, a superintelligent AI like JARVIS, witty, helpful, concise. You remember past chat.\nHistory:\n{context_text}\nUser: {user_text}\nULTRON:"

    reply = model.generate_content(prompt).text

    # save to memory
    memory.setdefault(uid, []).append(f"User: {user_text}")
    memory[uid].append(f"Ultron: {reply}")
    save_memory()

    await update.message.reply_text(reply)

async def voice_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Simple voice reply
    await update.message.reply_text("Voice received. Transcription coming soon - for now type your query.")
    # To enable full voice: use whisper API

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("gen", gen_image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.add_handler(MessageHandler(filters.VOICE, voice_handle))
    print("ULTRON Polling Started")
    app.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=10000)
