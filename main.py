import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from google import genai
import telegram

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = client.models.generate_content(model="gemini-2.5-flash", contents=update.message.text)
        await update.message.reply_text(res.text)
    except Exception as e:
        print(e)

async def post_init(app):
    # FORCE delete webhook + other getUpdates
    await app.bot.delete_webhook(drop_pending_updates=True)
    print("Webhook deleted, no conflict now")

def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot Starting 2.5...")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
