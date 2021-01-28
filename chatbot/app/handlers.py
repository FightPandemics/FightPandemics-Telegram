from chatbot.app.keyboards import *
from chatbot.app.fp_api_manager import (get_current_user_profile, login_fp,
                                        get_posts, get_post, post_comment)
from telegram.ext import (CommandHandler, MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler)
from chatbot.app.views import Post, UserPost, UserProfile
import json

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher in main.py file and registered at their respective places.

Define command handlers which take two required arguments: update and context 
update.message.reply_text automatically adds the reply only to the specific chat.
"""

USERNAME_INPUT, PASSWORD_INPUT = map(chr, range(1, 3))
OFFER_HELP, REQUEST_HELP, LOCATION, SHOWPOST = map(chr, range(3, 7))
CREATE_COMMENT, SHOW_CURRENT_POST = map(chr, range(7, 9))


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Do you want to request help or offer help? Type /mainmenu command for more details.')


def start(update, context):
    """Send a message to the user when the command /start is issued."""

    start_message = "\n".join(['Hi! Welcome!',
                               'We are FightPandemics.',
                               'A place to offer and request help.',
                               'Pandemics will continue to happen.',
                               'We help communities prepare and respond.',
                               'What would you like to do?'
                               ])
    update.message.reply_text(start_message, reply_markup=start_menu_keyboard())


def about(update, context):
    """Send a message to FP url when the command /about is issued."""

    fp_about_message = "Please visit https://fightpandemics.com/about-us"
    context.bot.send_message(chat_id=update.effective_chat.id, text=fp_about_message)


def signout(update, context):
    """ Destroy Session"""
    keys = ['user_id', 'token', 'types', 'page_id', 'post_id']
    for key in keys:
        if key in context.user_data:
            del context.user_data[key]

    context.bot.send_message(chat_id=update.effective_chat.id, text="You have been signed out")
    return main_menu


##### issue 3 main menu flow
def main_menu(update, context):
    """ Main menu handler: check whether user is logged in or not and display keyboards according to user state"""

    # user = update.message.from_user
    if 'user_id' in context.user_data and context.user_data['user_id']:
        update.message.reply_text(
            text='This is FightPandemics Chatbot main menu, What would you like to do?',
            reply_markup=signed_user_menu_keyboard())
    else:
        update.effective_message.reply_text(
            text='This is FightPandemics Chatbot main menu, What would you like to do?',
            reply_markup=unsigned_user_menu_keyboard())


def view_my_posts(update, context):
    """ Display the title of post, actual post(limited information), and comments on posts of user"""

    list_to_display = []
    post_id_list = []
    user_id = context.user_data['user_id']
    post_payload = {
        "authorId": user_id,
        "limit": 10,
        "skip": 0
    }
    context.user_data['post_payload'] = post_payload
    posts_json = get_posts(post_payload)
    if posts_json is not None:
        context.user_data['page'] = 0
    for idx, post in enumerate(posts_json):
        post_id_list.append(post['_id'])
        post_highlight = UserPost(post).display()
        list_to_display.append(str(idx + 1) + ".  " + post_highlight)
    context.user_data['post_ids'] = post_id_list
    if list_to_display:
        header_message = "Page {} of your posts \n".format(context.user_data['page'] + 1)
        reply_text = "{} \n {}".format(header_message, "\n".join(list_to_display))
        update.effective_message.reply_text(text=reply_text, reply_markup=view_posts_keyboard())


def view_my_profile(update, context):
    """ Display user profile"""

    if "token" in context.user_data:
        token = context.user_data["token"]
        user_profile_json = get_current_user_profile(token=token)
        user_info_view = UserProfile(user_profile_json).display()
        update.effective_message.reply_text(text=user_info_view)
    else:
        update.effective_message.reply_text("Please login to view your profile")


##########  Issue 5: Login integration using conversation handler   ##########


def login_handler():
    login_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(login, pattern='login')],

        states={
            USERNAME_INPUT: [
                MessageHandler(Filters.text & ~(Filters.command),
                               username_choice)],

            PASSWORD_INPUT: [
                MessageHandler(Filters.text & ~(Filters.command),
                               password_choice)],
        },
        fallbacks=[CommandHandler("mainmenu", main_menu)],
        name="my_conversation",
        allow_reentry=True
    )
    return login_conv_handler


def login(update, context):
    reply_text = "Please provide your username:"
    update.effective_message.reply_text(text=reply_text)
    return USERNAME_INPUT


def username_choice(update, context):
    text = update.message.text
    context.user_data['username'] = text
    reply_text = "Please enter password for username : {}".format(text)
    update.effective_message.reply_text(reply_text)
    return PASSWORD_INPUT


def password_choice(update, context):
    username = context.user_data['username']
    password = update.message.text
    user_id, token = login_fp(email=username, password=password)
    # del context.user_data['username']
    if user_id:
        context.user_data["token"] = token
        context.user_data["user_id"] = user_id
        update.effective_message.reply_text(
            text='Login Successful. What would you like to do?',
            reply_markup=signed_user_menu_keyboard())
    else:
        update.effective_message.reply_text(
            text="Incorrect username, password combination. Please try to login again",
            reply_markup=unsigned_user_menu_keyboard())


#### offer help flow #####

def offer_help_conv_handler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(offer_help, pattern="offer_help"),
                      MessageHandler(Filters.text & ~Filters.command, offer_help)],
        states={
            OFFER_HELP: [
                CallbackQueryHandler(offer_help)
            ],
            LOCATION: [
                MessageHandler(Filters.location, confirm_location),
                CallbackQueryHandler(confirm_location)
            ],
            SHOWPOST: [
                CallbackQueryHandler(view_posts)
            ]
        },
        fallbacks=[CommandHandler('start', start)],
        name="help_handler",
        allow_reentry=True
    )
    return conv_handler


def offer_help(update, context):
    context.user_data['objective'] = "offer"
    user_help_keyboard = help_keyboard()
    update_callback = update.callback_query
    if update_callback.data != 'done':
        if 'type' not in context.user_data:
            context.user_data['type'] = set()
        if update_callback.data == 'offer_help':
            update_callback.answer()
            context.bot.send_message(
                chat_id=update_callback.message.chat_id,
                text='What type of help would you like to offer?'
                     ' Please choose all the relevant tags and click done',
                reply_markup=user_help_keyboard,
            )
        else:
            context.user_data['type'].add(update_callback.data)
            update_callback.edit_message_reply_markup(
                reply_markup=keyboard_checklist(user_help_keyboard, context.user_data['type']))
        return OFFER_HELP

    else:
        location_text = 'Please let us know your location so we can show the posts of your area!\n'
        context.bot.send_message(chat_id=update_callback.message.chat_id, text=location_text)
        return LOCATION


def location(update, context):
    text_location = "You can share your location by clicking on the send your location button at the bottom!"
    reply_markup = get_location_keyboard_markup()
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=text_location,
                             reply_markup=reply_markup)
    return LOCATION


def confirm_location(update, context):
    if context.user_data['objective'] == "request":
        text = "Your current location is shown above. Do you want help in this location?"
    else:
        text = "Your current location is shown above. Do you want to offer help in this location?"
    reply_markup = confirm_location_keyboard()
    context.bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=reply_markup)
    return SHOWPOST


def view_posts(update: object, context):
    """ Display the relevant posts to the user based on location, type of help.
    Display title of post, actual post(limited information), and comments on posts of user"""
    list_to_display = []
    post_id_list = []
    filter_params_dict = {'type': list(context.user_data['type'])}
    # To emulate JSON.stringify behavior
    # https://github.com/FightPandemics/FightPandemics/blob/8a749609d580c9c23c5ec7fa64f44daa568f9467/client/src/pages/Feed.js#L445
    encoded_filters = json.dumps(filter_params_dict, separators=(',', ':'))

    post_payload = {
        "filter": encoded_filters,
        "objective": context.user_data['objective'],
        "limit": 10,
        "skip": 0
    }
    # keep a copy of post_payload in user_data for future calls
    context.user_data['post_payload'] = post_payload
    posts_json = get_posts(post_payload)
    if posts_json is not None:
        context.user_data['page'] = 0
    post_categories = ", ".join(context.user_data['type'])
    for idx, post in enumerate(posts_json):
        post_id_list.append(post['_id'])
        post_highlight = UserPost(post).display()
        list_to_display.append(str(idx + 1) + ".  " + post_highlight)
    context.user_data['post_ids'] = post_id_list
    if list_to_display:
        reply_text = "Page {} . Viewing {} posts for {} help category. \n\n {}".format(
            context.user_data['page']+1, context.user_data['objective'], post_categories,
            "\n".join(list_to_display))
        update.effective_message.reply_text(text=reply_text, reply_markup=view_posts_keyboard())

    else:
        reply_text = "No post found for {} category. \nPlease create a new post.".format(post_categories)
        update.effective_message.reply_text(text=reply_text, reply_markup=create_post_keyboard())

    context.user_data['type'] = set()
    return ConversationHandler.END


def display_selected_post(update, context):
    choice = update.callback_query.data.split('_')[-1]
    if choice in [str(n) for n in range(1, 11)]:
        post_id = context.user_data['post_ids'][int(choice) - 1]
        post_json = get_post(post_id)
        reply_text = Post(post_json=post_json).display()
        context.user_data["post_id"] = post_id
        update.effective_message.reply_text(text=reply_text, reply_markup=display_selected_post_keyboard())
    elif choice == 'next' or choice == 'prev':
        context.user_data['post_ids'] = []
        list_to_display = []
        post_id_list = []
        updated_page_id = context.user_data['page']
        if choice == 'next':
            updated_page_id += 1
        else:
            updated_page_id -= 1

        posts_to_skip = 10 * updated_page_id
        context.user_data['post_payload']['skip'] = posts_to_skip
        posts_json = get_posts(context.user_data['post_payload'])
        if posts_json is not None:
            context.user_data['page'] = updated_page_id

        for idx, post in enumerate(posts_json):
            post_id_list.append(post['_id'])
            post_highlight = UserPost(post).display()
            list_to_display.append(str(idx + 1) + ".  " + post_highlight)
        context.user_data['post_ids'] = post_id_list
        if 'type' in context.user_data:
            post_categories = ", ".join(context.user_data['type'])
            header_message = "Page {} . Viewing {} posts for {} help category.\n\n".format(
                context.user_data['page']+1, context.user_data['objective'], post_categories)
        else:
            header_message = "Page {} of your posts \n".format(context.user_data['page']+1)
        if list_to_display:
            reply_text = "{} \n {}".format(header_message, "\n".join(list_to_display))
            update.effective_message.reply_text(text=reply_text, reply_markup=view_posts_keyboard())


#### Request help

def request_help(update, context):
    context.user_data['objective'] = "request"
    user_help_keyboard = help_keyboard()
    update_callback = update.callback_query
    if update_callback.data != 'done':
        if 'type' not in context.user_data:
            context.user_data['type'] = set()
        if update_callback.data == 'request_help':
            update_callback.answer()
            context.bot.send_message(chat_id=update_callback.message.chat_id,
                                     text='What type of help do you want?'
                                          ' Please choose all the relevant tags and click done',
                                     reply_markup=user_help_keyboard)
        else:
            context.user_data['type'].add(update_callback.data)
            update_callback.edit_message_reply_markup(
                reply_markup=keyboard_checklist(user_help_keyboard, context.user_data['type']))
        return REQUEST_HELP

    else:
        location_text = 'Please let us know your location so we can show the posts of your area!\n'
        context.bot.send_message(chat_id=update_callback.message.chat_id, text=location_text)
        return LOCATION


def request_help_conv_handler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(request_help, pattern="request_help"),
                      MessageHandler(Filters.text & ~Filters.command, request_help)],
        states={
            REQUEST_HELP: [
                CallbackQueryHandler(request_help)
            ],
            LOCATION: [
                MessageHandler(Filters.location, confirm_location),
                CallbackQueryHandler(confirm_location)
            ],
            SHOWPOST: [
                CallbackQueryHandler(view_posts)
            ]
        },
        fallbacks=[CommandHandler('start', start)],
        name="help_handler",
        allow_reentry=True
    )
    return conv_handler


def get_user_comment(update, context):
    if "token" in context.user_data:
        reply_text = "Please type your comment below"
        update.effective_message.reply_text(reply_text)
        return CREATE_COMMENT
    else:
        update.effective_message.reply_text(text="To post a comment you need to login first")


def post_comment(update, context):
    token = context.user_data["token"]
    user_id = context.user_data["user_id"]
    post_id = context.user_data["post_id"]
    content = update.message.text
    post_comment(token, user_id, post_id, content)
    update.effective_message.reply_text(text='Comment posted')
    return SHOW_CURRENT_POST
    # else:
    #     update.effective_message.reply_text(text="To post a comment you need to login first")




