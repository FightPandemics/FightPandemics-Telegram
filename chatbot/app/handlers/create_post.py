import logging
from enum import Enum, auto

from telegram.ext import (
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)

from chatbot.app import handlers, keyboards, patterns, user_data, views
from chatbot.app.handlers import util
from .post_utils import (
    get_show_categories_callback,
    get_handle_pick_category_callback,
    get_handle_categories_done_callback,
    get_confirm_location_callback,
    get_no_location_callback,
    ask_user_to_sign_in,
)


class State(Enum):
    TITLE = auto()
    DESCRIPTION = auto()
    ASK_CATEGORIES = auto()
    CHOOSE_CATEGORIES = auto()
    LOCATION = auto()
    VISIBILITY = auto()
    DURATION = auto()
    PREVIEW = auto()
    CONFIRM_PREVIEW = auto()
    SUBMIT_POST = auto()
    EDIT_POST = auto()


def create_post_conversation():
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(_show_types, pattern=patterns.CREATE_POST),
            CallbackQueryHandler(
                _ask_for_title(pattern=patterns.REQUEST_HELP),
                pattern=patterns.REQUEST_HELP,
            ),
            CallbackQueryHandler(
                _ask_for_title(pattern=patterns.OFFER_HELP),
                pattern=patterns.OFFER_HELP,
            ),
        ],
        states={
            State.TITLE: [
                CallbackQueryHandler(_ask_for_title()),
            ],
            State.DESCRIPTION: [
                MessageHandler(Filters.text, _ask_for_description),
            ],
            State.ASK_CATEGORIES: [
                MessageHandler(Filters.text, _show_categories())
            ],
            State.CHOOSE_CATEGORIES: [
                CallbackQueryHandler(_categories_done(), pattern=patterns.DONE),
                CallbackQueryHandler(_pick_category()),
            ],
            State.LOCATION: [
                CallbackQueryHandler(_no_location()),
                MessageHandler(Filters.location | Filters.text, _confirm_location()),
            ],
            State.VISIBILITY: [
                CallbackQueryHandler(_ask_for_visibility),
            ],
            State.DURATION: [
                CallbackQueryHandler(_ask_for_duration),
            ],
            State.PREVIEW: [
                CallbackQueryHandler(_preview),
            ],
            State.CONFIRM_PREVIEW: [
                CallbackQueryHandler(_confirm_preview),
            ],
            State.SUBMIT_POST: [
                CallbackQueryHandler(_submit_post),
            ],
            State.EDIT_POST: [
                CallbackQueryHandler(_edit_post),
            ],
        },
        fallbacks=[handlers.MainMenuCmdHandler],
        name="create_post_handler",
        allow_reentry=True,
    )


def _show_types(update, context):
    if not user_data.is_user_signed_in(context=context):
        ask_user_to_sign_in(update, context)
        return ConversationHandler.END
    util.reply(
        update=update,
        context=context,
        text="Do you want to create a post to Offer Help or Request Help?",
        keyboard=keyboards.request_or_offer(),
    )
    return State.ASK_CATEGORIES,


def _show_categories():
    def handle_previous(update, context):
        context.user_data[user_data.POST_DESCRIPTION] = update.message.text

    return get_show_categories_callback(
        text='What type of help would you like to {}?'
             ' Please choose all the relevant tags and click done',
        state=_state_after(State.ASK_CATEGORIES),
        handle_previous=handle_previous,
    )


def _pick_category():
    return get_handle_pick_category_callback(
        state=State.CHOOSE_CATEGORIES,
    )


def _categories_done():
    return get_handle_categories_done_callback(
        text='Please let us know your location so we can show the posts of your area! '
             'Either type in your address manually or share it using the 📎 below. '
             'If you don\'t want to share your location, click the button below.',
        state=_state_after(State.CHOOSE_CATEGORIES),
    )


def _no_location():
    return get_no_location_callback(
        state=_state_after(State.LOCATION),
    )


def _confirm_location():
    return get_confirm_location_callback(
        state=_state_after(State.LOCATION),
        text="Your current location is shown above. Do you want to {} help in this location?"
    )


def _ask_for_title(pattern=None):
    def ask_for_title(update, context):
        if not user_data.is_user_signed_in(context=context):
            ask_user_to_sign_in(update, context)
            return ConversationHandler.END
        _reset_create_post_user_data(context=context)
        if pattern is None:
            local_pattern = update.callback_query.data
        else:
            local_pattern = pattern
        context.user_data[user_data.POST_OBJECTIVE] = user_data.objective_from_pattern(local_pattern)
        util.reply(
            update=update,
            context=context,
            text='What is the title of your post? (60 characters or less)',
        )
        return _state_after(State.TITLE)
    return ask_for_title


def _reset_create_post_user_data(context):
    for key in user_data.POST_INFO:
        context.user_data.pop(key, None)


def _ask_for_description(update, context):
    context.user_data[user_data.POST_TITLE] = update.message.text
    util.reply(
        update=update,
        context=context,
        text='What is the description of your post?',
    )
    return _state_after(State.DESCRIPTION)


def _ask_for_visibility(update, context):
    location = _get_user_location(context=context)
    if location is None:
        text = 'Since you have not specific a location this post will be shown worldwide.'
        keyboard = keyboards.continue_keyboard()
    else:
        text = 'What is the visibility of your post?'
        keyboard = keyboards.visibility()
    util.reply(
        update=update,
        context=context,
        text=text,
        keyboard=keyboard,
    )
    return _state_after(State.VISIBILITY)


def _ask_for_duration(update, context):
    visibility = update.callback_query.data
    if visibility == patterns.CONTINUE:
        visibility = "Wordwide"
    context.user_data[user_data.POST_VISIBILITY] = visibility
    util.reply(
        update=update,
        context=context,
        text='What is the duration of your post?',
        keyboard=keyboards.duration(),
    )
    return _state_after(State.DURATION)


def _preview(update, context):
    context.user_data[user_data.POST_DURATION] = update.callback_query.data
    util.reply(
        update=update,
        context=context,
        text='Press preview to preview your post',
        keyboard=keyboards.preview(),
    )
    return _state_after(State.PREVIEW)


def _confirm_preview(update, context):
    text = _format_preview(context=context)
    # TODO handle preview reply properly
    warning = "\n\nTODO rest of conversation not implemented yet"
    text += warning
    util.reply(
        update=update,
        context=context,
        text=text,
        # TODO should add keyboard so user can edit or submit etc
    )
    logging.warning(warning)
    # TODO should then check if user wants to edit or submit
    return State.SUBMIT_POST


def _format_preview(context):
    title = context.user_data[user_data.POST_TITLE]
    description = context.user_data[user_data.POST_DESCRIPTION]
    categories = context.user_data[user_data.POST_CATEGORIES]
    location = context.user_data.get(user_data.LOCATION)
    user_name = context.user_data[user_data.USERNAME]
    return _format_preview_from_data(
        title=title,
        description=description,
        categories=categories,
        user_name=user_name,
        location=location,
    )


def _format_preview_from_data(title, description, categories, user_name, location=None):
    data = {
        "post": {
            user_data.POST_TITLE: title,
            user_data.AUTHOR: {
                user_data.AUTHOR_NAME: user_name,
                user_data.LOCATION: location,
            },
            user_data.POST_CATEGORIES: categories,
            user_data.POST_DESCRIPTION: description,
            user_data.NUM_COMMENTS: 0,
        },
    }
    return views.Post(post_json=data).display()


def _submit_post(update, context):
    raise NotImplementedError


def _edit_post(update, context):
    raise NotImplementedError


def _state_after(current_state):
    states = list(State)
    for i, state in enumerate(states):
        if state == current_state:
            return states[i + 1]


def _get_user_location(context):
    return context.user_data.get(user_data.LOCATION)


CreatePostConvHandler = create_post_conversation()
