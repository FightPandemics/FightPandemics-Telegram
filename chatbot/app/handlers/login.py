import logging
from enum import Enum, auto

from telegram.ext import (
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)

from chatbot.app import handlers, keyboards, patterns, user_data
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
    handlers.util.reply(
        update=update,
        context=context,
        text=reply_text,
    )
    return State.USERNAME_INPUT


def username_choice(update, context):
    username = update.message.text
    context.user_data[user_data.USERNAME] = username
    reply_text = "Please enter password for username \"{}\":".format(username)
    handlers.util.reply(
        update=update,
        context=context,
        text=reply_text,
    )
    return State.PASSWORD_INPUT


def password_choice(update, context):
    username = context.user_data[user_data.USERNAME]
    password = update.message.text
    response = fpapi.login_fp(email=username, password=password)

    if isinstance(response, fpapi.Error):
        is_user_signed_in = False
        if response == fpapi.Error.INVALID_LOGIN:
            reply_text = "Incorrect username, password combination. Please try to login again"
        else:
            reply_text = "Something went wrong, could not connect to FightPandemics"
        logging.warning(f"Unable to login, got the error {response}. Showing user {reply_text}")
    else:
        user_id = response['user']['id']
        token = response['token']
        context.user_data[user_data.TOKEN] = token
        context.user_data[user_data.USER_ID] = user_id
        reply_text = 'Login Successful. What would you like to do?'
        is_user_signed_in = True

    handlers.util.reply(
        update=update,
        context=context,
        text=reply_text,
        keyboard=keyboards.main_menu(is_user_signed_in),
    )
    return ConversationHandler.END


def signout(update, context):
    """ Destroy Session"""
    for key in user_data.ALL_INFO:
        context.user_data.pop(key, None)

    reply_text = "You have been signed out"
    handlers.util.reply(
        update=update,
        context=context,
        text=reply_text,
        keyboard=keyboards.main_menu(is_user_signed_in=False),
    )


LoginConvHandler = login_conversation(pattern=patterns.LOGIN)
SignoutQueryHandler = CallbackQueryHandler(signout, pattern=patterns.SIGNOUT)
