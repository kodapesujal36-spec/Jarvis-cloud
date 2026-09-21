import asyncio

async def chat(update, context):
    prompt = update.message.text
    await update.message.chat.send_action(action="typing")

    MODELS = ["gemini-3.6-flash", "gemini-2.5-flash"]

    for model_name in MODELS:
        try:
            print(f"Trying {model_name}")
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model_name,
                contents=prompt
            )
            await update.message.reply_text(response.text)
            return

        except Exception as e:
            print(f"{model_name} failed: {e}")
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                continue  # busy, try next model (2.5)
            else:
                await update.message.reply_text(f"Error: {e}")
                return

    await update.message.reply_text("Google busy, try after 30 sec 🙏")
