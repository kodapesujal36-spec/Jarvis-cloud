import os, sys, threading
from flask import Flask

print("=== Checking ENV ===")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print(f"BOT_TOKEN exists: {bool(BOT_TOKEN)}")
print(f"GEMINI_API_KEY exists: {bool(GEMINI_API_KEY)}")

if not BOT_TOKEN:
    print("FATAL: BOT_TOKEN missing! Add in Render Environment")
    sys.exit(1)
if not GEMINI_API_KEY:
    print("FATAL: GEMINI_API_KEY missing! Add in Render Environment")
    sys.exit(1)

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("Gemini Client OK")
except Exception as e:
    print(f"Gemini Client FAIL: {e}")
    sys.exit(1)

web_app = Flask(__name__)
@web_app.route('/')
def home():
    return "JARVIS Running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("JARVIS Online Sir 🤖")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        prompt = f"You are JARVIS. Witty. User: {update.message.text}"
        r = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        await update.message.reply_text(r.text[:4000])
    except Exception as e:
        print(f"Chat error: {e}")
        await update.message.reply_text(f"Error: {e}")

def run_bot():
    print("Starting Telegram Bot...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    print(f"Web server on {port}")
    web_app.run(host="0.0.0.0", port=port)
