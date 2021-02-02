from telegram.ext import CommandHandler

from chatbot.app import keyboards


def main_menu(update, context):
    """ Main menu handler: check whether user is logged in or not and display keyboards according to user state"""

    text = 'This is FightPandemics Chatbot main menu, What would you like to do?'
    is_user_signed_in = context.user_data.get('user_id') is not None
    update.message.reply_text(
        text=text,
        reply_markup=keyboards.main_menu(is_user_signed_in),
    )


def start(update, context):
    """Send a message to the user when the command /start is issued."""

    start_message = "\n".join(['Hi! Welcome!',
                               'We are FightPandemics.',
                               'A place to offer and request help.',
                               'Pandemics will continue to happen.',
                               'We help communities prepare and respond.',
                               'What would you like to do?'
                               ])
    update.message.reply_text(
        text=start_message,
        reply_markup=keyboards.request_or_offer(),
    )


MainMenuCmdHandler = CommandHandler("mainmenu", main_menu)
StartCmdHandler = CommandHandler("start", main_menu)
