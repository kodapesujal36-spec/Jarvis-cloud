import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

app = Flask(__name__)
@app.route('/')
def home(): return "Jarvis Live - Gemini 3.8 Flash"

def run_flask():
 app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-3.8-flash"
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update, context):
 await update.message.reply_text("Hi! I am Jarvis 🤖 Gemini 3.8 Flash!")

async def ai_reply(update, context):
 try:
  resp = client.models.generate_content(model=MODEL, contents=update.message.text)
  await update.message.reply_text(resp.text)
 except Exception as e:
  await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
 application = Application.builder().token(TOKEN).build()
 application.add_handler(CommandHandler("start", start))
 application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
 application.run_polling()
