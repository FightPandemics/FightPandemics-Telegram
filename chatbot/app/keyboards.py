from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardMarkup, ReplyKeyboardRemove
import emoji

CATEGORIES = ["Medical Supplies", "Groceries/Food", "Business", "Education", "Legal", "Wellbeing/Mental",
              "Entertainment", "Information", "Funding", "R&D", "Tech", "Others"]


# define all keyboards here.
def start_menu_keyboard():
    """ display this keyboard with response message when /start command is typed by user"""

    keyboard = [[InlineKeyboardButton('Request Help', callback_data='request_help'),
                 InlineKeyboardButton('Offer Help', callback_data='offer_help')]]
    return InlineKeyboardMarkup(keyboard)


def help_keyboard():
    keyboard = [[InlineKeyboardButton('Groceries/Food', callback_data='Groceries/Food'),
                 InlineKeyboardButton('Medical Supplies', callback_data='Medical Supplies'),
                 InlineKeyboardButton('Funding/Donate', callback_data='Funding/Donate')],
                [InlineKeyboardButton('Well-being/Mental', callback_data='Well-being/Mental'),
                 InlineKeyboardButton('Information', callback_data='Information'),
                 InlineKeyboardButton('Tech', callback_data='Tech')],
                [InlineKeyboardButton('Legal', callback_data='Legal'),
                 InlineKeyboardButton('Education', callback_data='Education'),
                 InlineKeyboardButton('Business', callback_data='Business')],
                [InlineKeyboardButton('Done', callback_data='done')]]
    return InlineKeyboardMarkup(keyboard)


def signed_user_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Request Help', callback_data='request_help'),
                 InlineKeyboardButton('Offer Help', callback_data='offer_help')],
                [InlineKeyboardButton('View My Posts', callback_data='view_my_posts'),
                 InlineKeyboardButton('View My Profile', callback_data='view_my_profile')],
                [InlineKeyboardButton('Create Post', callback_data='create_post'),
                 InlineKeyboardButton('About FightPandemics', callback_data='about')],
                [InlineKeyboardButton('Signout', callback_data='signout')]]

    return InlineKeyboardMarkup(keyboard)


def unsigned_user_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Request Help', callback_data='request_help'),
                 InlineKeyboardButton('Offer Help', callback_data='offer_help')],
                [InlineKeyboardButton('View My Posts', callback_data='view_my_posts'),
                 InlineKeyboardButton('View My Profile', callback_data='view_my_profile')],
                [InlineKeyboardButton('Create Post', callback_data='create_post'),
                 InlineKeyboardButton('About FightPandemics', callback_data='about')],
                [InlineKeyboardButton('Login', callback_data='login')]]
    return InlineKeyboardMarkup(keyboard)


def keyboard_checklist(user_help_keyboard, user_selected_types):
    outer_length = len(user_help_keyboard.inline_keyboard)
    for i in range(outer_length):
        inner_length = len(user_help_keyboard.inline_keyboard[i])
        for j in range(inner_length):
            current_button = user_help_keyboard.inline_keyboard[i][j]["text"]
            if current_button in user_selected_types:
                user_help_keyboard.inline_keyboard[i][j] = InlineKeyboardButton(
                    emoji.emojize(current_button + ' :rocket: '),
                    callback_data=current_button)

    return user_help_keyboard


def confirm_location_keyboard():
    keyboard = [[InlineKeyboardButton('Confirm', callback_data='view_posts')]]
                 #InlineKeyboardButton('Type in different Location', callback_data='location')]]
    return InlineKeyboardMarkup(keyboard)


def get_location_keyboard_markup():
    location_keyboard = KeyboardButton(text="Send Live Location",
                                       request_location=True)  # creating location button object
    custom_keyboard = [[location_keyboard]]  # creating keyboard object
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
    return reply_markup


def view_posts_keyboard():
    keyboard = [[InlineKeyboardButton('1', callback_data='display_selected_post_1'),
                 InlineKeyboardButton('2', callback_data='display_selected_post_2'),
                 InlineKeyboardButton('3', callback_data='display_selected_post_3'),
                 InlineKeyboardButton('4', callback_data='display_selected_post_4'),
                 InlineKeyboardButton('5', callback_data='display_selected_post_5')],
                [InlineKeyboardButton('6', callback_data='display_selected_post_6'),
                 InlineKeyboardButton('7', callback_data='display_selected_post_7'),
                 InlineKeyboardButton('8', callback_data='display_selected_post_8'),
                 InlineKeyboardButton('9', callback_data='display_selected_post_9'),
                 InlineKeyboardButton('10', callback_data='display_selected_post_10')],
                [InlineKeyboardButton('< Prev', callback_data='display_selected_post_prev'),
                 InlineKeyboardButton('Create Post', callback_data='create_post'),
                 InlineKeyboardButton('Next > ', callback_data='display_selected_post_next')]]
    return InlineKeyboardMarkup(keyboard)


def display_selected_post_keyboard():
    keyboard = [[InlineKeyboardButton('See Comments', callback_data='see_comments'),
                 InlineKeyboardButton('View Author Profile', callback_data='view_author_profile'),
                 InlineKeyboardButton('Post Comment', callback_data='post_comment')]]
    return InlineKeyboardMarkup(keyboard)


def create_post_keyboard():
    keyboard = [[InlineKeyboardButton('Create Post', callback_data='create_post')]]
    return InlineKeyboardMarkup(keyboard)


def share_location_keyboard():
    keyboard = [[InlineKeyboardButton('Yes, I would like to share my live location', callback_data='confirm_location')],
                [InlineKeyboardButton('I will enter my address manually', callback_data='location')]]
    return InlineKeyboardMarkup(keyboard)