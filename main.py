import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

JARVIS = "You are JARVIS, Tony Stark's AI. Witty, loyal, advanced. Answer concisely."

# Models priority - 3.6 busy then 2.5
MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b" # This one NEVER gets 503
]

async def get_reply(prompt):
    for model_name in MODELS:
        try:
            print(f"Trying {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text, model_name
        except Exception as e:
            print(f"{model_name} failed: {e}")
            if "503" in str(e) or "UNAVAILABLE" in str(e) or "429" in str(e):
                await asyncio.sleep(1) # Wait 1 sec before next model
                continue
            continue
    return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("JARVIS Online, Sir. Systems at 100%. 🤖\nTry talking to me!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        prompt = f"{JARVIS}\nUser: {update.message.text}\nJARVIS:"
        text, used_model = await get_reply(prompt)

        if text is None:
            await update.message.reply_text("⚠️ All models busy (503). Sir, Google servers are overloaded. Try again in 5 seconds. Auto-switching to 1.5-8b...")
            return

        print(f"Answered by {used_model}")
        await update.message.reply_text(text[:4000])

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Sir, my processors need a moment. Try again.")

def main():
    print("🚀 JARVIS 2.5 STARTING...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
