import os, asyncio, threading
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "OK"

async def start(u,c): await u.message.reply_text("JARVIS Online")
async def chat(u,c):
    r = client.models.generate_content(model="gemini-2.0-flash", contents=u.message.text)
    await u.message.reply_text(r.text[:4000])

async def bot_main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

threading.Thread(target=lambda: asyncio.run(bot_main()), daemon=True).start()
flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
