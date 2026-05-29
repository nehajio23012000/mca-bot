import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

TOKEN = os.getenv("TOKEN")

# ⚠️ APNI DETAILS YAHAN BADLEIN ⚠️
GROUP_LINK = "https://t.me/+nFgeD6LLU9A2MmY1"
ADMIN_ID = 8565742151  # Yahan apni real admin ID dalein

# Part 1 mein banaye gaye links yahan dalein
QR_URL = "YAHAN_APNA_QR_CODE_LINK_DALEIN"
VIDEO_URL = "YAHAN_APNA_VIDEO_LINK_DALEIN"

waiting_users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎥 Demo Video", callback_data="demo")],
        [InlineKeyboardButton("💳 Buy Access ₹49", callback_data="buy")],
        [InlineKeyboardButton("✅ Verify Payment", callback_data="verify")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome To MCA New C-Product\n\nNeeche diye gaye buttons select karein:",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "demo":
        await query.message.reply_video(video=VIDEO_URL, caption="▶️ Demo Video")
    elif query.data == "buy":
        await query.message.reply_photo(photo=QR_URL, caption="⚠️ Pay ₹49 via QR Code\n\nPayment ke baad 'Verify Payment' par click karke UTR number bhejein.")
    elif query.data == "verify":
        waiting_users[query.from_user.id] = True
        await query.message.reply_text("✏️ Apna 12-digit UTR / Transaction Number bhejein:")

async def receive_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in waiting_users:
        utr_text = update.message.text
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 *New Payment Request*\n\nUser ID: `{user_id}`\nUTR: `{utr_text}`\n\nApprove karne ke liye is command ko copy karke send karein:\n`/approve {user_id}`",
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ Details submit ho gayi hain! Admin approval ka wait karein.")
        del waiting_users[user_id]

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    try:
        target_user_id = int(context.args[0])
        await context.bot.send_message(
            chat_id=target_user_id,
            text=f"🎉 *Payment Approved!*\n\nGroup join karne ke liye niche link par click karein:\n{GROUP_LINK}",
            parse_mode="Markdown"
        )
        await update.message.reply_text(f"✅ User {target_user_id} approved!")
    except Exception:
        await update.message.reply_text("❌ Use karein: `/approve user_id`")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve", approve))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_payment))

print("Bot is running...")
app.run_polling()
