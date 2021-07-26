import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, \
    MessageHandler, Filters

# constants
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TO_UPPER, TO_LOWER, BACK = range(3)


def start(update, context):
    upper_button = InlineKeyboardButton(
        text='mayúsculas'.upper(),
        callback_data='to_upper'
    )
    lower_button = InlineKeyboardButton(
        text='minúsculas'.lower(),
        callback_data='to_lower'
    )
    update.message.reply_text(
        text=f'Holaaaa {update.message.chat.first_name}',
        reply_markup=InlineKeyboardMarkup([
            [upper_button, lower_button]
        ])
    )


# callbacks
def back_callback(update, context):
    query = update.callback_query
    upper_button = InlineKeyboardButton(
        text='mayúsculas'.upper(),
        callback_data='to_upper'
    )
    lower_button = InlineKeyboardButton(
        text='minúsculas'.lower(),
        callback_data='to_lower'
    )
    query.edit_message_text(
        text=f'Holaaaa {query.message.chat.first_name}',
        reply_markup=InlineKeyboardMarkup([
            [upper_button, lower_button]
        ])
    )
    return ConversationHandler.END


def to_upper_callback(update, context):
    query = update.callback_query
    back_button = InlineKeyboardButton(
        text='Atrás',
        callback_data='back'
    )
    query.edit_message_text(
        text='Mayúsculas: introduzca un texto',
        reply_markup=InlineKeyboardMarkup([
            [back_button]
        ])
    )
    return TO_UPPER


def to_lower_callback(update, context):
    query = update.callback_query
    back_button = InlineKeyboardButton(
        text='Atrás',
        callback_data='back'
    )
    query.edit_message_text(
        text='Minúsculas: introduzca un texto',
        reply_markup=InlineKeyboardMarkup([
            [back_button]
        ])
    )
    return TO_LOWER


# conversations
def to_upper_conversation(update, context):
    update.message.reply_text(f'En mayúsculas: {update.message.text.upper()}')
    return ConversationHandler.END


def to_lower_conversation(update, context):
    update.message.reply_text(f'En minúsculas: {update.message.text.lower()}')
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(pattern='back', callback=back_callback))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern='to_upper', callback=to_upper_callback)
        ],
        states={
            TO_UPPER: [MessageHandler(Filters.text, to_upper_conversation)]
        },
        fallbacks=[
            CallbackQueryHandler(pattern='back', callback=back_callback)
        ],
        per_message=True
    ))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern='to_lower', callback=to_lower_callback)
        ],
        states={
            TO_LOWER: [MessageHandler(Filters.text, to_lower_conversation)]
        },
        fallbacks=[
            CallbackQueryHandler(pattern='back', callback=back_callback)
        ],
        per_message=True
    ))

    updater.start_polling()
    print('Bot is polling')
    updater.idle()
