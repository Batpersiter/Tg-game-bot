from flask import Flask, request
import os
import asyncio

app = Flask(__name__)

# Import bot setup
from bot import setup_bot

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    asyncio.run(app.bot.process_update(update))
    return 'OK', 200

@app.route('/health', methods=['GET'])
def health():
    return "🎮 SAS Game Bot is alive and ready to play!", 200

async def start_bot():
    application = setup_bot()
    await application.initialize()
    await application.start()

    # Set webhook
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await application.bot.set_webhook(url=webhook_url)
        print(f"✅ Webhook set to: {webhook_url}")
    else:
        print("❌ WEBHOOK_URL not set!")

    app.bot = application
    return app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app = asyncio.run(start_bot())
    app.run(port=port)
