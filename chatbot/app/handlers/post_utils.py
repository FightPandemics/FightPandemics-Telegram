import logging

from chatbot.app import keyboards, user_data
from chatbot.app.handlers import util


def get_show_categories_callback(text, state, handle_previous=None):
    """Returns a callback for showing post categories.

    Any {} will be replaced with the objective in the text string
    """
    def show_categories(update, context):
        if handle_previous is not None:
            objective = handle_previous(update, context)
        objective = context.user_data[user_data.POST_OBJECTIVE]
        context.user_data[user_data.POST_CATEGORIES] = set()
        util.reply(
            update=update,
            context=context,
            text=_format_text(text, objective),
            keyboard=keyboards.help_categories(),
        )
        return state
    return show_categories


def _format_text(text, objective):
    objectives = [objective] * text.count('{}')
    return text.format(*objectives)


def get_handle_categories_done_callback(text, state):
    def handle_categories_done(update, context):
        """Handle user is done picking help categories"""
        util.reply(
            update=update,
            context=context,
            text='Please let us know your location so we can show the posts of your area! '
                 'Either type in your address manually or share it using the 📎 below. '
                 'If you don\'t want to share your location, click the button below.',
            keyboard=keyboards.no_location(),
        )
        return state
    return handle_categories_done


def get_handle_pick_category_callback(state):
    def handle_pick_category(update, context):
        """Handle user picks a help category"""
        categories = context.user_data.get(user_data.POST_CATEGORIES, set())
        categories.add(update.callback_query.data)
        context.user_data[user_data.POST_CATEGORIES] = categories
        update.callback_query.edit_message_reply_markup(
            reply_markup=keyboards.checklist(
                keyboards.help_categories(),
                categories,
            ),
        )
        return state
    return handle_pick_category


def get_no_location_callback(state):
    def handle_no_location(update, context):
        """User does not want to share location, proceed to show posts"""
        util.reply(
            update=update,
            context=context,
            text="No location given, is this correct?",
            keyboard=keyboards.confirm_location(),
        )
        return state
    return handle_no_location


def get_confirm_location_callback(text, state):
    """Returns a callback for confirm_location

    Any {} will be replaced with the objective in the text string
    """
    def confirm_location(update, context):
        location = _get_location_from_message(update.message)
        if location is None:
            _handle_location_fail(update, context)
            return state
        context.user_data[user_data.LOCATION] = _get_location_from_message(update.message)
        objective = context.user_data[user_data.POST_OBJECTIVE]
        util.reply(
            update=update,
            context=context,
            text=_format_text(text, objective),
            keyboard=keyboards.confirm_location(),
        )
        return state
    return confirm_location


def _handle_location_fail(update, context):
    util.reply(
        update=update,
        context=context,
        text="Couldn't parse the location, continuing without location...",
        keyboard=keyboards.confirm_location(),
    )


def _get_location_from_message(message):
    if message.location:
        longitude = message.location.longitude
        latitude = message.location.latitude
        logging.warning(f"Got location (longitude={longitude}, latitude={latitude}) but lookup not yet implemented")
        # TODO we should lookup the location
        # probably using the function chatbot.app.fp_api_manager.get_user_location
        # until this is done, return None for now
        return None
    elif message.text:
        logging.warning("Location from text message not yet implemented")
        return None
    raise NotImplementedError


def ask_user_to_sign_in(update, context):
    util.reply(
        update=update,
        context=context,
        text='Please sign in to create a post',
        keyboard=keyboards.main_menu(is_user_signed_in=False),
    )
