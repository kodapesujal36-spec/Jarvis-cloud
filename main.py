import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
app = Flask(__name__)
@app.route('/')
def home(): return "AI Jarvis is Live!"
def run_flask():
 app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
TOKEN = os.environ.get("BOT_TOKEN")
async def start(update, context):
 await update.message.reply_text("Hi! I am AI Jarvis 🤖\nAsk anything!")
async def ai_reply(update, context):
 try:
   resp = model.generate_content(update.message.text)
   await update.message.reply_text(resp.text)
 except Exception as e:
   await update.message.reply_text(f"Error: {e}")
if __name__ == "__main__":
 application = Application.builder().token(TOKEN).build()
 application.add_handler(CommandHandler("start", start))
 application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
 application.run_polling()
