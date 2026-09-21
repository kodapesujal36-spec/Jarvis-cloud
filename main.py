import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    if not prompt:
        return
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    MODELS = ["gemini-2.5-flash", "gemini-2.0-flash"]  # 2.5 first = no 503

    # If you want 3.6 first, use this:
    # MODELS = ["gemini-3.0-flash", "gemini-2.5-flash"]

    for model_name in MODELS:
        try:
            print(f"Trying {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            await update.message.reply_text(response.text)
            return
        except Exception as e:
            print(f"{model_name} failed: {e}")
            continue

    await update.message.reply_text("Google busy, try after 30 sec 🙏")

def main():
    print("Bot starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
