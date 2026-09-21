import os, threading
from flask import Flask
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Jarvis is Live!"

async def start(update, context):
    await update.message.reply_text("Hi! I am Jarvis 🚀")

async def chat(update, context):
    try:
        prompt = update.message.text
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    application.run_polling(drop_pending_updates=True)

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app_flask.run(host="0.0.0.0", port=10000)
