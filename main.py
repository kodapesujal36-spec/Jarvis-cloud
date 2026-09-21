import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

JARVIS = "You are JARVIS, Tony Stark's AI. Witty, loyal, advanced. Answer concisely."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("JARVIS Online, Sir. Systems at 100%. 🤖\nTry talking to me!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        prompt = f"{JARVIS}\nUser: {update.message.text}\nJARVIS:"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        await update.message.reply_text(response.text[:4000])
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Sir, my processors need a moment. Try again.")

def main():
    print("🚀 OLD JARVIS STARTING...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    # drop_pending_updates=True fixes conflict
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
