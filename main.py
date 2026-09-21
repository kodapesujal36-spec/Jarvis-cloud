import os
import asyncio
import threading
from flask import Flask
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# USE v1 API - This fixes 404 error!
client = genai.Client(
    api_key=GEMINI_KEY,
    http_options={"api_version": "v1"}
)

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Jarvis is Live! 🚀"

async def start(update, context):
    await update.message.reply_text("Hi! I am Jarvis 🚀 How can I help?")

async def chat(update, context):
    try:
        prompt = update.message.text
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # NEWEST stable model!
            contents=prompt
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def run_flask():
    app_flask.run(host="0.0.0.0", port=10000)

async def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    await application.bot.delete_webhook(drop_pending_updates=True)
    print("Webhook deleted - Starting polling!")
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    print("Bot Started!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(run_bot())
