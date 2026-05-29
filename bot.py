from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import os

TOKEN = os.getenv("TOKEN")

GROUP_LINK = "https://t.me/+nFgeD6LLU9A2MmY1"

ADMIN_ID = 8565742151

waiting_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🎥 Demo Video", callback_data="demo")],
        [InlineKeyboardButton("💳 Buy Access ₹49", callback_data="buy")],
        [InlineKeyboardButton("✅ Verify Payment", callback_data="verify")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to MCA New C-Product",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "demo":

        await query.message.reply_video(
            video=open("demo.mp4", "rb"),
            caption="Demo Video"
        )

    elif query.data == "buy":

        await query.message.reply_photo(
            photo=open("qr.png", "rb"),
            caption="Pay ₹49 and click Verify Payment"
        )

    elif query.data == "verify":

        waiting_users[query.from_user.id] = True

        await query.message.reply_text(
            "Send your UTR Number or Payment Screenshot"
        )

async def receive_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id in waiting_users:

        text = update.message.text

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Payment request from {user_id}\nUTR: {text}"
        )

        await update.message.reply_text(
            "Payment submitted. Wait for approval."
        )

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"Payment Approved ✅\nJoin Group:\n{GROUP_LINK}"
        )

        await update.message.reply_text("User Approved")

    except:
        await update.message.reply_text("Use: /approve user_id")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve", approve))

app.add_handler(CallbackQueryHandler(buttons))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, receive_payment)
)

print("Bot Running...")

app.run_polling()
