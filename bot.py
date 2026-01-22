import os
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext
)

FULL_NAME, EMAIL, PHONE, AVAILABILITY = range(4)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID"))

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🚗 Tesla Demo Drive\n\n"
        "Please send your Full Name:\n\n"
        "By continuing, you agree to be contacted regarding a Tesla demo drive."
    )
    return FULL_NAME

def full_name(update: Update, context: CallbackContext):
    context.user_data["Full Name"] = update.message.text
    update.message.reply_text("📧 Please send your Email Address:")
    return EMAIL

def email(update: Update, context: CallbackContext):
    context.user_data["Email"] = update.message.text
    update.message.reply_text("📱 Please send your Phone Number:")
    return PHONE

def phone(update: Update, context: CallbackContext):
    context.user_data["Phone"] = update.message.text
    update.message.reply_text(
        "🕒 What is your availability for a demo drive?\n"
        "Example: Weekdays after 5pm, Weekends"
    )
    return AVAILABILITY

def availability(update: Update, context: CallbackContext):
    context.user_data["Availability"] = update.message.text

    data = context.user_data

    update.message.reply_text(
        "✅ Thank you!\n\n"
        "I’ll contact you shortly to confirm your Tesla demo drive."
    )

    update.message.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            "🚨 New Tesla Demo Drive Lead\n\n"
            f"Name: {data['Full Name']}\n"
            f"Email: {data['Email']}\n"
            f"Phone: {data['Phone']}\n"
            f"Availability: {data['Availability']}"
        )
    )

    return ConversationHandler.END

updater = Updater(BOT_TOKEN, use_context=True)

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        FULL_NAME: [MessageHandler(Filters.text & ~Filters.command, full_name)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
        PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)],
        AVAILABILITY: [MessageHandler(Filters.text & ~Filters.command, availability)],
    },
    fallbacks=[],
)

updater.dispatcher.add_handler(conv)
updater.start_polling()
updater.idle()
