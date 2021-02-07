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


MainMenuCmdHandler = CommandHandler("mainmenu", main_menu)
