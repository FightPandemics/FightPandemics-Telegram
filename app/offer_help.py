
import emoji
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from keyboards import help_keyboard
from geopy.geocoders import Nominatim

updater = Updater(token='1361186628:AAGshG-2bsygAPpqBinJ910ceaGYvTMFpNg', use_context=True)
dispatcher = updater.dispatcher
keyboard_offer_help = help_keyboard()

HELP, LOCATION, END = range(3)

offer_text = 'Hi Welcome! ' \
       'We are fight Pandemics. ' \
       'A place to offer and request help.  Pandemics will ' \
       'continue to happen. ' \
       'We will help communities prepare and respond. ' \
       '' \
       'What would you like to do?'

location_text = 'Please let us know your location so we can share the resources closest to you!\n' \
                'You can share your location by clicking on the send your location button at the bottom!'


def print_keyboard(keys):
    outer_length = len(keys["inline_keyboard"])
    for i in range(outer_length):
        inner_length = len(keys["inline_keyboard"][i])
        for j in range(inner_length):
            print(keys["inline_keyboard"][i][j])




def welcome_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Request Help', callback_data='request_help')],
               [InlineKeyboardButton('Offer Help', callback_data='offer_help')]]
    return InlineKeyboardMarkup(keyboard)


def other_help_keyboard():
    keyboard = [[InlineKeyboardButton('Groceries/food', callback_data='Groceries/food')],
                [InlineKeyboardButton('Medical Supplies', callback_data='Medical Supplies')],
                [InlineKeyboardButton('Funding/Donate', callback_data='Funding/Donate')],
                [InlineKeyboardButton('Well-being/Mental', callback_data='Well-being/Mental')],
                [InlineKeyboardButton('Information', callback_data='Information')],
                [InlineKeyboardButton('Technology', callback_data='Technology')],
                [InlineKeyboardButton('Legal', callback_data='Legal')],
                [InlineKeyboardButton('Education', callback_data='Education')],
                [InlineKeyboardButton('Business', callback_data='Business')],
                [InlineKeyboardButton('Done', callback_data='Done')]
        ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_checklist(keys, input):
    outer_length = len(keys.inline_keyboard)
    for i in range(outer_length):
        inner_length = len(keys.inline_keyboard[i])
        for j in range(inner_length):
            if keys["inline_keyboard"][i][j]["text"] == input:
                keys["inline_keyboard"][i][j] = InlineKeyboardButton(emoji.emojize(input + ' :thumbs_up:'),
                                                                     callback_data=input)
                return keys
            if keys["inline_keyboard"][i][j]["text"] == emoji.emojize(input + ' :thumbs_up:'):
                keys["inline_keyboard"][i][j] = InlineKeyboardButton(input, callback_data=input)
                return keys
    return keys


def find_emoji(word):
    for w in word:
        if any(char in emoji.UNICODE_EMOJI for char in w):
            return True
    return False

def find_keyboard_emojis(keys):
    outer_length = len(keys["inline_keyboard"])
    for i in range(outer_length):
        inner_length = len(keys["inline_keyboard"][i])
        for j in range(inner_length):
            if find_emoji(keys["inline_keyboard"][i][j]["text"]):
                print(keys["inline_keyboard"][i][j]["callback_data"])


def start(update, context):
    update.message.reply_text(offer_text, reply_markup=welcome_menu_keyboard())

    return HELP


# def location(update, context):
#     location_keyboard = KeyboardButton(text="send_location", request_location=True)  # creating location button object
#     contact_keyboard = KeyboardButton('Share contact', request_contact=True)  # creating contact button object
#     custom_keyboard = [[location_keyboard, contact_keyboard]]  # creating keyboard object
#     reply_markup = ReplyKeyboardMarkup(custom_keyboard)
#     update.message.reply_text(
#         "Would you mind sharing your location and contact with me?",
#         reply_markup=reply_markup)
#
#     return ConversationHandler.END


def offer_help(update, context):
    update = update.callback_query
    update.answer()
    if update.data != 'done':
        update.edit_message_reply_markup(reply_markup=keyboard_checklist(keyboard_offer_help, update.data))
        return HELP
    else:
        find_keyboard_emojis(keyboard_offer_help)
        location_keyboard = KeyboardButton(text="send_location",
                                           request_location=True)  # creating location button object
        contact_keyboard = KeyboardButton('Share contact', request_contact=True)  # creating contact button object
        custom_keyboard = [[location_keyboard]]  # creating keyboard object
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        context.bot.send_message(chat_id=update.message.chat_id, text=location_text, reply_markup=reply_markup)
        return LOCATION


def location_start(update, context):
    update = update.callback_query

    return LOCATION


def location_message(update, context):
    print(update.message.location)
    text_location = "Your current location is "
    keyboard = [[InlineKeyboardButton('Confirm', callback_data="confirm")],
                [InlineKeyboardButton('I will enter my location manually', callback_data='offer_help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text=text_location, reply_markup=reply_markup)

    return LOCATION


def confirm_message(update, context):
    update = update.callback_query
    context.bot.send_message(chat_id=update.message.chat_id, text="Confirm")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start',start)],
    states={
        HELP: [CallbackQueryHandler(offer_help)
               ],
        LOCATION: [
                   MessageHandler(Filters.location, location_message),
                   CallbackQueryHandler(confirm_message, pattern="confirm")
        ],


    },
    fallbacks=[CommandHandler('start',start)]

)

# start_handler = CommandHandler('start', start)
# location_handler = MessageHandler(Filters.location, location_message)
# handler = CallbackQueryHandler(offer_help)
# confirm_handler = CallbackQueryHandler(confirm_message, pattern="confirm")
#
# #
dispatcher.add_handler(conv_handler)
# dispatcher.add_handler(start_handler)
# dispatcher.add_handler(location_handler)
# dispatcher.add_handler(handler)
# dispatcher.add_handler(confirm_handler)
updater.start_polling()



test = emoji.emojize("Test :thumbs_up:")

# x = emoji.UNICODE_EMOJI in test






