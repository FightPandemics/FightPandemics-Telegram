from telegram.ext import CommandHandler, CallbackQueryHandler

from chatbot.app import keyboards, user_data, patterns
from chatbot.app.handlers import util


def main_menu(update, context):
    """ Main menu handler: check whether user is logged in or not and display keyboards according to user state"""

    text = 'This is FightPandemics Chatbot main menu, What would you like to do?'
    user_signed_in = user_data.is_user_signed_in(context=context)
    if not user_signed_in:
        text += " To see more options, create posts etc you need to first login."
    util.reply(
        update=update,
        context=context,
        text=text,
        keyboard=keyboards.main_menu(user_signed_in),
    )


MainMenuCmdHandler = CommandHandler("mainmenu", main_menu)
MainMenuQueryHandler = CallbackQueryHandler(main_menu, pattern=patterns.MAINMENU)
