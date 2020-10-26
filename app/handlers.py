from app.keyboards import (start_menu_keyboard, signed_user_menu_keyboard,
                           unsigned_user_menu_keyboard, help_keyboard, keyboard_checklist,
                           confirm_location_keyboard, get_location_keyboard_markup)
from app.fp_api_manager import get_user_posts, get_current_user_profile, login_fp, get_posts
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler, ConversationHandler)

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher in main.py file and registered at their respective places.

Define command handlers which take two required arguments: update and context 
update.message.reply_text automatically adds the reply only to the specific chat.
"""

USERNAME_INPUT, PASSWORD_INPUT = map(chr, range(2))
HELP, LOCATION, SHOWPOST = map(chr, range(2,5))


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


##### issue 3 main menu flow
def main_menu(update, context):
    """ Main menu handler: check whether user is logged in or not and display keyboards according to user state"""

    # user = update.message.from_user
    if 'logged_in' in context.user_data and context.user_data['logged_in']:
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
    posts_json = get_user_posts()
    for idx, post in enumerate(posts_json):
        list_to_display.append(str(idx + 1) + ". " + post['title'] + "- " +
                               post['content'] + "- " +
                               str(post['commentsCount']) + " comments")

    update.effective_message.reply_text(
        text="\n".join(list_to_display))


def view_profile(update, context):
    """ Display user profile"""

    if "token" in context.user_data:
        user_info_list = []
        token = context.user_data["token"]
        user_profile_json = get_current_user_profile(token=token)
        print(user_profile_json)
        user_info_list.append("Name: " + user_profile_json['firstName'] + " " + user_profile_json['lastName'])
        is_volunteer = "No"
        if user_profile_json['objectives']['volunteer']:
            is_volunteer = "Yes"

        user_info_list.append("Volunteer : " + is_volunteer)
        update.effective_message.reply_text(
            text="\n".join(user_info_list))

    else:
        update.effective_message.reply_text("Please login to view your profile")


def request_help(update, context):
    """Send a message when the command /start is issued."""

    # update.message.reply_text('what kind of help do you want?')
    update.effective_message.reply_text(
        text="what kind of help do you want?",
        reply_markup=help_keyboard())


########## Issue 5: Login integration using conversation handler ##########

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
        name="my_conversation"
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
    update.message.reply_text(reply_text)
    return PASSWORD_INPUT


def password_choice(update, context):
    password = update.message.text
    username = context.user_data['username']
    user_id, token = login_fp(email=username, password=password)
    del context.user_data['username']
    if user_id:
        context.user_data["token"] = token
        context.user_data["user_id"] = user_id
        update.message.reply_text(
            text='Login Successful. What would you like to do?',
            reply_markup=signed_user_menu_keyboard())
    else:
        update.message.reply_text(
            text="Incorrect username, password combination. Please try to login again",
            reply_markup=unsigned_user_menu_keyboard())


#### offer help flow #####

user_help_keyboard = help_keyboard()


def offer_help_conv_handler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(offer_help, pattern="offer_help"),
                      MessageHandler(Filters.text & ~Filters.command, offer_help)],
        states={
            HELP: [
                CallbackQueryHandler(offer_help)
            ],
            LOCATION: [
                MessageHandler(Filters.location, location)
            ],
            SHOWPOST: [
                CallbackQueryHandler(view_posts)
            ]
        },
        fallbacks=[CommandHandler('start', start)],
        name="help_handler"
    )
    return conv_handler


def offer_help(update, context):
    global user_help_keyboard
    if user_help_keyboard is None:
        user_help_keyboard = help_keyboard()
    update_callback = update.callback_query
    if update_callback.data != 'done':
        if 'type' not in context.user_data:
            context.user_data['type'] = []
        if update_callback.data != 'offer_help':
            context.user_data['type'].append(update_callback.data)

        update_callback.edit_message_reply_markup(
            text='What type of help would you like to offer? Please choose all the relevant tags?',
            reply_markup=keyboard_checklist(user_help_keyboard, update_callback.data))
        return HELP
    else:
        location_text = 'Please let us know your location so we can display the posts of your area!\n' \
                        'You can share your location by clicking on the send your location button at the bottom!'
        reply_markup = get_location_keyboard_markup()
        context.bot.send_message(chat_id=update_callback.message.chat_id, text=location_text, reply_markup=reply_markup)
        return LOCATION


def location(update, context):
    text_location = "Your current location is shown above. Do you want to offer help in the same area."
    location_confirm_markup = confirm_location_keyboard()
    context.bot.send_message(chat_id=update.message.chat_id, text=text_location, reply_markup=location_confirm_markup)
    return SHOWPOST


def view_posts(update, context):
    """ Display the relevant posts to the user based on location, type of help.
    Display title of post, actual post(limited information), and comments on posts of user"""
    list_to_display = []
    filter_params_dict = {'type': context.user_data['type']}
    posts_json = get_posts(filter_params_dict, objective='request')
    for idx, post in enumerate(posts_json):
        list_to_display.append(str(idx + 1) + ". " + post['title'] + "- " +
                               post['content'] + "- " +
                               str(post['commentsCount']) + " comments")
    if list_to_display:
        update.effective_message.reply_text(text="\n".join(list_to_display))
    else:
        post_categories = ", ".join(context.user_data['type'])
        update.effective_message.reply_text(text="No post found for {} category. Please create a new post.".format(post_categories))
    del context.user_data['type']
    return ConversationHandler.END


def create_posts(update, context):
    if "token" in context.user_data:
        token = context.user_data["token"]
        user_profile_json = get_current_user_profile(token=token)
    else:
        update.effective_message.reply_text(text="To create posts you need to login first")
