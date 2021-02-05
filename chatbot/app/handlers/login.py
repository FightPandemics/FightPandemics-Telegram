from enum import Enum, auto

from telegram.ext import (
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)

from chatbot.app import handlers, keyboards, patterns
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
    handlers.util.reply_to_callback_query(
        update=update,
        context=context,
        text=reply_text,
    )
    return State.USERNAME_INPUT


def username_choice(update, context):
    username = update.message.text
    context.user_data['username'] = username
    reply_text = "Please enter password for username \"{}\":".format(username)
    handlers.util.reply_to_callback_query(
        update=update,
        context=context,
        text=reply_text,
    )
    return State.PASSWORD_INPUT


def password_choice(update, context):
    username = context.user_data['username']
    password = update.message.text
    user_id, token = fpapi.login_fp(email=username, password=password)

    if user_id:
        context.user_data["token"] = token
        context.user_data["user_id"] = user_id
        reply_text = 'Login Successful. What would you like to do?'
        is_user_signed_in = True
    else:
        reply_text = "Incorrect username, password combination. Please try to login again"
        is_user_signed_in = False

    handlers.util.reply_to_callback_query(
        update=update,
        context=context,
        text=reply_text,
        keyboard=keyboards.main_menu(is_user_signed_in),
    )
    return ConversationHandler.END


def signout(update, context):
    """ Destroy Session"""
    keys = ['user_id', 'token', 'types', 'page_id', 'post_id']
    for key in keys:
        context.user_data.pop(key, None)

    reply_text = "You have been signed out"
    handlers.util.reply_to_callback_query(
        update=update,
        context=context,
        text=reply_text,
        keyboard=keyboards.main_menu(is_user_signed_in=False),
    )


LoginConvHandler = login_conversation(pattern=patterns.LOGIN)
SignoutQueryHandler = CallbackQueryHandler(signout, pattern=patterns.SIGNOUT)
