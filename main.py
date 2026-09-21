import asyncio

async def chat(update, context):
    prompt = update.message.text
    await update.message.chat.send_action(action="typing")
    
    # Try BEST model 3 times with wait
    for attempt in range(3):
        try:
            print(f"Trying gemini-3.6-flash attempt {attempt+1}")
            # NEW - PASTE THIS
MODELS = ["gemini-2.5-flash", "gemini-3.6-flash"]

for model_name in MODELS:
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=user_message
        )
        print(f"Success with {model_name}")
        break
    except Exception as e:
        print(f"Failed {model_name}: {e}")
        continue
            )
            await update.message.reply_text(response.text)
            return  # Success!
            
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"503 busy, waiting 5 sec...")
                await asyncio.sleep(5)  # Wait 5 sec and retry
                continue
            else:
                await update.message.reply_text(f"Error: {e}")
                return
    
    # If 3 tries failed, use lite as backup (so user not left hanging)
    try:
        print("3.6 failed 3 times, using lite fallback")
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        await update.message.reply_text(response.text + "\n\n_(used lite because 3.6 busy)_")
    except Exception as e:
        await update.message.reply_text("Google AI very busy, please try after 1 minute 🙏")
