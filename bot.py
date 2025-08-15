from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Use environment variables (important for security on Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@sasgamecenter"
GROUP_CHAT_ID = -1002666383656  # Make sure this is correct

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/sasgamecenter")],
        [InlineKeyboardButton("👥 Join Group", url="https://t.me/+6vNF1zFG3OhjYjdl")],
        [InlineKeyboardButton("✅ I've Joined – Verify", callback_data="verify")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚨 To play the game, please join our channel and group, then click Verify:",
        reply_markup=reply_markup
    )

# Verify callback
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Always answer the callback query

    user_id = query.from_user.id

    try:
        channel_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        group_member = await context.bot.get_chat_member(chat_id=GROUP_CHAT_ID, user_id=user_id)

        if channel_member.status in ["member", "administrator", "creator"] and \
           group_member.status in ["member", "administrator", "creator"]:
            keyboard = [[InlineKeyboardButton("🎮 Play Tic-Tac-Toe", url="https://sasbottictactoe.netlify.app/")]]
            await query.edit_message_text(
                text="✅ You're verified! Click below to play 🎮",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.answer(
                "❌ You're not a member yet. Please join both the channel and group.",
                show_alert=True
            )
    except Exception as e:
        await query.answer("⚠️ Verification failed. Try again.", show_alert=True)
        print(f"Error: {e}")

# Entry point
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found. Set the environment variable.")
    else:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(verify_callback, pattern="^verify$"))
        print("Bot is running...")
        app.run_polling()
