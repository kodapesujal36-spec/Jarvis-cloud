import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai  # NEW library

app = Flask(__name__)
@app.route('/')
def home(): return "AI Jarvis Live - Gemini 3.8 Flash ⚡"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()

# NEW WAY - Gemini 3.8 Flash
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-3.8-flash"  # or "gemini-flash-latest"

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Hi! I am AI Jarvis 🤖\nPowered by Gemini 3.8 Flash!")

async def ai_reply(update, context):
    try:
        resp = client.models.generate_content(
            model=MODEL_ID,
            contents=update.message.text
        )
        await update.message.reply_text(resp.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def error_handler(update, context):
    print(f"Error: {context.error}")

if __name__ == "__main__":
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    app_bot.add_error_handler(error_handler)
    app_bot.run_polling()
