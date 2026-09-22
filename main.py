import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

JARVIS = "You are JARVIS, Tony Stark's AI. Witty, loyal, advanced. Answer concisely."

MODELS = ["gemini-2.0-flash", "gemini-1.5-flash-8b", "gemini-1.5-flash"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("JARVIS Online, Sir. Systems at 100%. 🤖")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    prompt = f"{JARVIS}\nUser: {update.message.text}\nJARVIS:"
    
    for model_name in MODELS:
        try:
            response = client.models.generate_content(model=model_name, contents=prompt)
            await update.message.reply_text(response.text[:4000])
            return
        except Exception as e:
            print(f"{model_name} busy: {e}")
            continue
    
    await update.message.reply_text("Sir, Google is busy (503). Trying again in 2 sec...")

def main():
    print("🚀 JARVIS 2.5 READY")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
