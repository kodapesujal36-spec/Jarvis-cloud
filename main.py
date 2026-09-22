import os, sys, asyncio, threading
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    print("Missing ENV")
    sys.exit(1)

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "JARVIS Running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("JARVIS Online Sir 🤖")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        prompt = f"You are JARVIS. User: {update.message.text}"
        r = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        await update.message.reply_text(r.text[:4000])
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def run_bot_async():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot polling started...")
    await app.run_polling(drop_pending_updates=True)

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot_async())

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)
