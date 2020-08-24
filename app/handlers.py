from app.keyboards import (welcome_menu_keyboard, signed_user_menu_keyboard,
                           unsinged_user_menu_keyboard, help_keyboard,
                           other_help_keyboard, login_keyboard)
from app.fp_api_manager import get_fp_post, get_current_user_profile

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
"""


def start(update, context):
    """Send a message to the user when the command /start is issued."""
    update.message.reply_text('Hi! Welcome!' + '\nWe are FightPandemics.' + '\nA place to offer and request help.' +
                              '\n' + '\nWhat would you like to do?',
                              reply_markup=welcome_menu_keyboard())


def about(update, context):
    """Send a message to FP url when the command /about is issued."""
    fp_about_message = "Please visit https://fightpandemics.com/about-us"
    context.bot.send_message(chat_id=update.effective_chat.id, text=fp_about_message)


# 3 main menu flow
def main_menu(update, context):
    """ Main menu handler: check whether user is logged in or not and display keyboards"""

    # user = update.message.from_user
    if 'logged_in' in context.user_data and context.user_data['logged_in']:
        update.message.reply_text(
            text='Main Menu: What would you like to do?',
            reply_markup=signed_user_menu_keyboard())
    else:
        update.effective_message.reply_text(
            text='Main Menu: What would you like to do?',
            reply_markup=unsinged_user_menu_keyboard())


def login_fp(update, context):
    """Send a message when the command /start is issued."""
    update.effective_message.reply_text(
        text="login",
        reply_markup=login_keyboard())


def view_posts(update, context):
    """ Display the title of post, actual post(limited information), and comments on posts of user"""
    list_to_display = []
    posts_json = get_fp_post()
    for idx, post in enumerate(posts_json):
        list_to_display.append(str(idx + 1) + ". " + post['title'] + "- " +
                               post['content'] + "- " +
                               str(post['commentsCount']) + " comments")

    update.effective_message.reply_text(
        text="\n".join(list_to_display))


def view_profile(update, context):
    """ Display user profile"""
    user_info_list = []
    user_profile_json = get_current_user_profile()
    user_info_list.append("Name: " + user_profile_json['firstName'] + " " + user_profile_json['lastName'])
    is_volunteer = "No"
    if user_profile_json['objectives']['volunteer']:
        is_volunteer = "Yes"

    user_info_list.append("Volunteer : " + is_volunteer)
    update.effective_message.reply_text(
        text="\n".join(user_info_list))


def request_help(update, context):
    """Send a message when the command /start is issued."""
    # update.message.reply_text('what kind of help do you want?')
    update.effective_message.reply_text(
        text="what kind of help do you want?",
        reply_markup=help_keyboard())


def offer_help_menu(update, context):
    update.effective_message.reply_text(
        text="What type of help would you like to offer?",
        reply_markup=help_keyboard())


def show_offer_other_help_menu(update, context):
    # query = update.callback_query
    # query.answer()
    update.effective_message.reply_text(
        text="What type of other help would you like to offer?",
        reply_markup=other_help_keyboard())
