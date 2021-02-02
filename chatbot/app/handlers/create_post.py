from enum import Enum, auto

from telegram.ext import (
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)

from chatbot.app import handlers, keyboards
from chatbot.app.handlers import util
from chatbot.app.patterns import Pattern
from chatbot.app.user_data import CATEGORIES_KEY
from chatbot.app.handlers import location


class State(Enum):
    TYPE = auto()
    CATEGORIES = auto()
    LOCATION = auto()
    SHOWPOST = auto()


def create_post_conversation(pattern):
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(create_post, pattern=pattern),
        ],
        states={
            State.TYPE: [
                CallbackQueryHandler(handle_type)
            ],
            State.CATEGORIES: [
                CallbackQueryHandler(handle_categories_done, pattern=Pattern.DONE),
                CallbackQueryHandler(handle_pick_category),
            ],
            State.LOCATION: [
                CallbackQueryHandler(handle_no_location),
                MessageHandler(Filters.location | Filters.text, confirm_location),
            ],
            State.SHOWPOST: [
                handlers.ViewPostsQueryHandler,
            ]
        },
        fallbacks=[handlers.StartCmdHandler],
        name="help_handler",
        allow_reentry=True
    )


def create_post(update, context):
    reply = "Do you want to make a post to Offer Help or Request Help?"
    util.reply_to_callback_query(
        update=update,
        context=context,
        text=reply,
        keyboard=keyboards.request_or_offer(),
    )
    return State.TYPE


def handle_type(update, context):
    """Handle uses chooses to request or offer help"""
    pattern = update.callback_query.data
    objective = "request" if pattern == Pattern.OFFER_HELP else "offer"
    context.user_data['objective'] = objective
    util.reply_to_callback_query(
        update=update,
        context=context,
        text='What type of help would you like to offer?'
             ' Please choose all the relevant tags and click done',
        keyboard=keyboards.help_categories(),
    )
    return State.CATEGORIES


def handle_pick_category(update, context):
    """Handle user picks a help category"""
    categories = context.user_data.get(CATEGORIES_KEY, set())
    categories.add(update.callback_query.data)
    context.user_data[CATEGORIES_KEY] = categories
    update.callback_query.edit_message_reply_markup(
        reply_markup=keyboards.checklist(
            keyboards.help_categories(),
            categories,
        ),
    )
    return State.CATEGORIES


def handle_categories_done(update, context):
    """Handle user is done picking help categories"""
    util.reply_to_callback_query(
        update=update,
        context=context,
        text='Please let us know your location so we can show the posts of your area! '
             'Either type in your address manually or share it using the 📎 below. '
             'If you don\'t want to share your location, click the button below.',
        keyboard=keyboards.no_location(),
    )
    return State.LOCATION


def confirm_location(update, context):
    context.user_data['location'] = get_location_from_message(update.message)

    if context.user_data['objective'] == "request":
        text = "Your current location is shown above. Do you want help in this location?"
    else:
        text = "Your current location is shown above. Do you want to offer help in this location?"
    reply_markup = keyboards.confirm_location()
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=reply_markup,
    )
    return State.SHOWPOST


def get_location_from_message(message):
    if message.location:
        return message.location
    elif message.text:
        raise NotImplementedError
    raise NotImplementedError


def handle_no_location(update, context):
    """User does not want to share location, proceed to show posts"""
    util.reply_to_callback_query(
        update=update,
        context=context,
        text="No location given, is this correct?",
        keyboard=keyboards.confirm_location(),
    )
    return State.SHOWPOST


CreatePostConvHandler = create_post_conversation(pattern=Pattern.CREATE_POST)
