from flask import Flask, request
from telegram.ext import ApplicationBuilder, WebhookUpdater
import os

app = Flask(__name__)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-render-url.onrender.com/webhook

# Import bot handlers (defined in bot.py)
from bot import setup_bot

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    asyncio.run(app.bot.process_update(update))
    return 'OK', 200

@app.route('/health', methods=['GET'])
def health():
    return "Bot is alive!", 200

async def start_webhook():
    global app
    application = setup_bot()
    await application.initialize()
    await application.start()

    # Set webhook
    await application.bot.set_webhook(url=WEBHOOK_URL)

    # Attach application to Flask
    app.bot = application
    return app

# Run this in main
if __name__ == "__main__":
    import asyncio
    app = asyncio.run(start_webhook())
    app.run(port=int(os.getenv("PORT", 8080)))
