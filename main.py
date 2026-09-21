import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        await update.message.reply_text(res.text)
    except Exception as e:
        print(e)
        await update.message.reply_text("Try again 🙏")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot Started with 2.5-flash")
    app.run_polling()

if __name__ == "__main__":
    main()
def main():
    print("Bot starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
