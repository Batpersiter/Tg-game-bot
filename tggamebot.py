from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = 'BOT_TOKEN' #Replace with your BOT_TOKEN
CHANNEL_USERNAME = '@sasgamecenter' #Replace with your CHANNEL_USERNAME
GROUP_CHAT_ID = -1002666383656  # Replace with your actual group ID

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/sasgamecenter")], #Replace with your Channel_Link
        [InlineKeyboardButton("👥 Join Group", url="https://t.me/+6vNF1zFG3OhjYjdl")], #Replace with your Channel_Link
        [InlineKeyboardButton("✅ I've Joined – Verify", callback_data="verify")]
    ]
    await update.message.reply_text(
        "🚨 To play the game, please join our channel and group, then click Verify:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Verify button handler
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    # Check membership in channel and group
    channel_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
    group_member = await context.bot.get_chat_member(chat_id=GROUP_CHAT_ID, user_id=user_id)

    if channel_member.status in ["member", "administrator", "creator"] and \
       group_member.status in ["member", "administrator", "creator"]:
        keyboard = [
            [InlineKeyboardButton("🎮 Play Tic-Tac-Toe", url="https://sasbottictactoe.netlify.app/")] # Replace with your game web URL 
        ]
        await query.edit_message_text(
            text="✅ You're verified! Click below to play 🎮",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.answer(
            "❌ You're not a member yet. Please join both the channel and group.",
            show_alert=True
        )

# Start the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
app.run_polling()