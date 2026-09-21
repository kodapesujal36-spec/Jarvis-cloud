# Don't use app.run_polling() on Render Web Service
# Use this:
import threading

def run_bot():
    app.run_polling()

threading.Thread(target=run_bot).start()
app_flask.run(host='0.0.0.0', port=10000)
