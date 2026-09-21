import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai
from google.genai import types

# --- CONFIG ---
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Set BOT_TOKEN and GEMINI_API_KEY in Render Environment!")

client = genai.Client(api_key=GEMINI_API_KEY)

# Memory {user_id: [messages]}
chat_memory = {}
MAX_HISTORY = 8

SYSTEM_PROMPT = "You are a helpful, friendly, concise AI assistant. Reply in same language user uses."

# --- COMMANDS ---
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ **Perfect AI Bot Ready!**\n\n"
        "Powered by `Gemini 2.5 Flash`\n\n"
        "• I remember our chat\n"
        "• Fast & No errors\n\n"
        "Commands:\n"
        "/start - Show this\n"
        "/clear - Clear memory\n"
        "/help - Help",
        parse_mode="Markdown"
    )

async def clear_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_memory.pop(update.effective_user.id, None)
    await update.message.reply_text("🧹 Memory cleared! Let's start fresh.")

# --- MAIN CHAT ---
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if not text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Manage memory
    if user_id not in chat_memory:
        chat_memory[user_id] = []

    chat_memory[user_id].append(types.Content(role="user", parts=[types.Part.from_text(text=text)]))

    # Keep only last N
    if len(chat_memory[user_id]) > MAX_HISTORY:
        chat_memory[user_id] = chat_memory[user_id][-MAX_HISTORY:]

    # Try models in order
    MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite"]

    for model in MODELS:
        try:
            logging.info(f"User {user_id} -> Trying {model}")
            response = client.models.generate_content(
                model=model,
                contents=chat_memory[user_id],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=2000
                )
            )

            reply_text = response.text
            # Save AI reply to memory
            chat_memory[user_id].append(types.Content(role="model", parts=[types.Part.from_text(text=reply_text)]))

            # Handle long messages
            if len(reply_text) > 4000:
                for x in range(0, len(reply_text), 4000):
                    await update.message.reply_text(reply_text[x:x+4000])
            else:
                await update.message.reply_text(reply_text)
            return

        except Exception as e:
            logging.warning(f"{model} failed: {e}")
            continue

    await update.message.reply_text("😔 AI is very busy right now. Please try again after 20 seconds.")
    # Remove last user message if failed
    if chat_memory[user_id]:
        chat_memory[user_id].pop()

# --- STARTUP ---
async def post_init(app: Application):
    await app.bot.delete_webhook(drop_pending_updates=True)
    logging.info("Webhook deleted - Conflict fixed")

def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("clear", clear_cmd))
    app.add_handler(CommandHandler("help", start_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))

    logging.info("🚀 ULTIMATE BOT STARTED - Gemini 2.5 Flash")
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
