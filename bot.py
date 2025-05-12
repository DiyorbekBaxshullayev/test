from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = 'BOT_TOKEN'
OPERATOR_CHAT_ID = CHAT_ID  # Operator Telegram ID

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Operatorga xabar
    message = f"🔔 Yangi foydalanuvchi start bosdi:\n\n👤 Ismi: {user.full_name}\n🆔 ID: {user.id}"
    await context.bot.send_message(chat_id=OPERATOR_CHAT_ID, text=message)

    # Telefon so‘rovchi tugma
    await update.message.reply_text(
        "Iltimos, telefon raqamingizni yuborish uchun quyidagi tugmani bosing.",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

# Telefon raqamni qabul qilish
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact

    # Operatorga yuborish
    message = (
        f"📞 Yangi foydalanuvchi raqamini yubordi:\n\n"
        f"👤 Ismi: {contact.first_name} {contact.last_name or ''}\n"
        f"📱 Telefon: {contact.phone_number}\n"
        f"🆔 ID: {contact.user_id}"
    )
    await context.bot.send_message(chat_id=OPERATOR_CHAT_ID, text=message)

    # Foydalanuvchiga javob va klaviaturani o‘chirish
    await update.message.reply_text(
        "Rahmat! Maʼlumotingiz qabul qilindi. Operator tez orada bogʻlanadi.",
        reply_markup=ReplyKeyboardRemove()
    )

# Botni ishga tushirish
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    app.run_polling()
