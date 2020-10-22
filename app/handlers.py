import logging

from keyboards import *
from fp_api_manager import get_user_posts, get_current_user_profile, login_fp

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler, ConversationHandler)

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher in main.py file and registered at their respective places.

Define command handlers which take two required arguments: update and context 
update.message.reply_text automatically adds the reply only to the specific chat.
"""

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

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


## issue 3 main menu flow
def main_menu(update, context):
    """ Main menu handler: check whether user is logged in or not and display keyboards according to user state"""

    # user = update.message.from_user
    if 'logged_in' in context.user_data and context.user_data['logged_in']:
        update.message.reply_text(
            text='This is main menu, What would you like to do?',
            reply_markup=signed_user_menu_keyboard())
    else:
        update.effective_message.reply_text(
            text='Main Menu: What would you like to do?',
            reply_markup=unsigned_user_menu_keyboard())


########## Issue 5: Login integration using conversation handler ##########


USERNAME_INPUT, PASSWORD_INPUT = range(2)


def login_handler():
    conv_handler = ConversationHandler(
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
    return conv_handler


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
            text="Incorrect username, password combination. Please try to login again",reply_markup=unsigned_user_menu_keyboard())


def view_posts(update, context):
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

    ''' update.message.reply_text('what kind of help do you want?')
    update.effective_message.reply_text(
        text="what kind of help do you want?",
        reply_markup=help_keyboard())'''
    update = update.callback_query

    if update.data != 'done':
        update.edit_message_reply_markup(reply_markup=keyboard_checklist(user_help_keyboard, update.data))
        
        return HELP

    else:
        update.message.reply_text('Please let us know your location so we can share the resources closest to you!\n\n' 'You can share your location by clicking on the attachment button and then choose to \n 1 - Send Live Location \n 2 - Send Custom Location Manually')

        return LOCATION


#### offer help flow #####
HELP, LOCATION = range(2)
user_help_keyboard = help_keyboard()


def offer_help(update, context):
    update = update.callback_query

    if update.data != 'done':
        update.edit_message_reply_markup(reply_markup=keyboard_checklist(user_help_keyboard, update.data))
        return HELP

    else:
        update.message.reply_text('Please let us know your location so we can share the resources closest to you!\n\n' 'You can share your location by clicking on the attachment button and then choose to \n 1 - Send Live Location \n 2 - Send Custom Location Manually')

        return LOCATION

def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    

def offer_help_conv_handler():
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(request_help, pattern='request_help')],
        states={
            HELP: [
                CallbackQueryHandler(request_help)
            ],
            LOCATION: [MessageHandler(Filters.location, location)],
        },

        fallbacks=[CommandHandler('start', start)]

    )
    return conv_handler


def create_posts(update,context):
    if "token" in context.user_data:
        user_info_list = []
        token = context.user_data["token"]
        user_profile_json = get_current_user_profile(token=token)
    else:
        update.effective_message.reply_text(text="To create posts you need to login first")
