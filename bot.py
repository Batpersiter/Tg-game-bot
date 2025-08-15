from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import json

# Bot config
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@sasgamecenter"
GROUP_CHAT_ID = -1002666383656
GAME_URL = "https://sasbottictactoe.netlify.app/"
ADMIN_USER_ID = 5769596731  # Your Telegram ID

# File to store user data
USERS_FILE = "users.json"

def load_users():
    """Load user data from JSON file"""
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    """Save user data to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# /start command with referral
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    users = load_users()

    # Track new user with referral
    if str(user_id) not in users:
        referrer = context.args[0] if context.args else "direct"
        users[str(user_id)] = {
            "name": first_name,
            "referrer": referrer,
            "joined": True
        }
        save_users(users)
        print(f"🆕 New user: {first_name} (ID: {user_id}) | Referred by: {referrer}")

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/sasgamecenter")],
        [InlineKeyboardButton("👥 Join Group", url="https://t.me/+6vNF1zFG3OhjYjdl")],
        [InlineKeyboardButton("✅ I've Joined – Verify", callback_data="verify")]
    ]
    await update.message.reply_text(
        f"👋 Hello {first_name}!\n\n"
        "🚨 To play the game, please join our channel and group, then click Verify:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Verify membership
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    first_name = query.from_user.first_name

    try:
        channel_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        group_member = await context.bot.get_chat_member(GROUP_CHAT_ID, user_id)

        if channel_member.status in ["member", "administrator", "creator"] and \
           group_member.status in ["member", "administrator", "creator"]:
            await query.edit_message_text(
                text=f"✅ Welcome, {first_name}! You're verified 🎉",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎮 Play Tic-Tac-Toe", url=GAME_URL)]
                ])
            )
        else:
            await query.edit_message_text(
                text="❌ You're not a member yet. Please join both the channel and group.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📢 Join Channel", url="https://t.me/sasgamecenter")],
                    [InlineKeyboardButton("👥 Join Group", url="https://t.me/+6vNF1zFG3OhjYjdl")],
                    [InlineKeyboardButton("✅ Try Again", callback_data="verify")]
                ])
            )
    except Exception as e:
        print(f"❌ Error verifying user {user_id}: {e}")
        await query.edit_message_text(
            "⚠️ Verification failed. Please try again.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔁 Try Again", callback_data="verify")]
            ])
        )

# Admin command: /stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You're not authorized to view stats.")
        return

    users = load_users()
    total = len(users)

    # Count referrals
    ref_counts = {}
    for data in users.values():
        ref = data["referrer"]
        ref_counts[ref] = ref_counts.get(ref, 0) + 1

    # Sort by count
    sorted_refs = sorted(ref_counts.items(), key=lambda x: x[1], reverse=True)

    msg = f"📊 **Total Users: {total}**\n\n"
    msg += "🔗 **Top Referrers:**\n"
    for ref, count in sorted_refs:
        msg += f"• `{ref}`: **{count}** user(s)\n"

    await update.message.reply_text(msg, parse_mode="Markdown")

# Setup bot
def setup_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="^verify$"))
    app.add_handler(CommandHandler("stats", stats))  # Admin stats
    return app
