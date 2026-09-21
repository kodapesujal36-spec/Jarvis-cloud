import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
BOT_TOKEN=os.environ.get("BOT_TOKEN")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("JARVIS ONLINE 24/7! Send any message.")
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"JARVIS: {update.message.text}")
app=ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
