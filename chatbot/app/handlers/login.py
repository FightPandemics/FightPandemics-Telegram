from enum import Enum, auto

from telegram.ext import (
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)

from chatbot.app import handlers, keyboards
from chatbot.app import fp_api_manager as fpapi


class State(Enum):
    USERNAME_INPUT = auto()
    PASSWORD_INPUT = auto()


def login_conversation(pattern):
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(login, pattern=pattern)],
        states={
            State.USERNAME_INPUT: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    username_choice,
                ),
            ],
            State.PASSWORD_INPUT: [
                MessageHandler(
                    Filters.text & ~(Filters.command),
                    password_choice,
                ),
            ],
        },
        fallbacks=[handlers.MainMenuCmdHandler],
        name="login_conversation",
        allow_reentry=True,
    )


def login(update, context):
    reply_text = "Please provide your username:"
    update.effective_message.reply_text(text=reply_text)
    return State.USERNAME_INPUT


def username_choice(update, context):
    text = update.message.text
    context.user_data['username'] = text
    reply_text = "Please enter password for username : {}".format(text)
    update.effective_message.reply_text(reply_text)
    return State.PASSWORD_INPUT


def password_choice(update, context):
    username = context.user_data['username']
    password = update.message.text
    user_id, token = fpapi.login_fp(email=username, password=password)

    if user_id:
        context.user_data["token"] = token
        context.user_data["user_id"] = user_id
        text = 'Login Successful. What would you like to do?',
        is_user_signed_in = True
    else:
        text = "Incorrect username, password combination. Please try to login again",
        is_user_signed_in = False

    update.effective_message.reply_text(
        text=text,
        reply_markup=keyboards.main_menu(is_user_signed_in),
    )
    return ConversationHandler.END


def signout(update, context):
    """ Destroy Session"""
    keys = ['user_id', 'token', 'types', 'page_id', 'post_id']
    for key in keys:
        if key in context.user_data:
            del context.user_data[key]

    context.bot.send_message(chat_id=update.effective_chat.id, text="You have been signed out")


LoginConvHandler = login_conversation(pattern='login')
SignoutQueryHandler = CallbackQueryHandler(signout, pattern='signout')
