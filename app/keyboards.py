from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardMarkup, ReplyKeyboardRemove
import emoji


# define all keyboards here.
def start_menu_keyboard():
    """ display this keyboard with response message when /start command is typed by user"""

    keyboard = [[InlineKeyboardButton('Request Help', callback_data='request_help'),
                 InlineKeyboardButton('Offer Help', callback_data='offer_help')]]
    return InlineKeyboardMarkup(keyboard)


def help_keyboard():
    keyboard = [[InlineKeyboardButton('Groceries/food', callback_data='Groceries/food'),
                 InlineKeyboardButton('Medical Supplies', callback_data='Medical Supplies'),
                 InlineKeyboardButton('Funding/Donate', callback_data='Funding/Donate')],
                [InlineKeyboardButton('Well-being/Mental', callback_data='Well-being/Mental'),
                 InlineKeyboardButton('Information', callback_data='Information'),
                 InlineKeyboardButton('Technology', callback_data='Technology')],
                [InlineKeyboardButton('Legal', callback_data='Legal'),
                 InlineKeyboardButton('Education', callback_data='Education'),
                 InlineKeyboardButton('Business', callback_data='Business')],
                [InlineKeyboardButton('Done', callback_data='done')]]
    return InlineKeyboardMarkup(keyboard)


def signed_user_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Offer Help', callback_data='offer_help'),
                 InlineKeyboardButton('Request Help', callback_data='request_help')],
                [InlineKeyboardButton('View My Posts', callback_data='view_posts'),
                 InlineKeyboardButton('View My Profile', callback_data='view_profile')],
                [InlineKeyboardButton('Create posts', callback_data='create_posts'),
                 InlineKeyboardButton('About FightPandemics', callback_data='about')],
                [InlineKeyboardButton('Signout', callback_data='signout')]]

    return InlineKeyboardMarkup(keyboard)


def unsigned_user_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Offer Help', callback_data='offer_help'),
                 InlineKeyboardButton('Request Help', callback_data='request_help')],
                [InlineKeyboardButton('View My Posts', callback_data='view_posts'),
                 InlineKeyboardButton('View My Profile', callback_data='view_profile')],
                [InlineKeyboardButton('Create posts', callback_data='create_posts'),
                 InlineKeyboardButton('About FightPandemics', callback_data='about')],
                [InlineKeyboardButton('Login', callback_data='login')]]
    return InlineKeyboardMarkup(keyboard)


def keyboard_checklist(user_help_keyboard, input_data):
    outer_length = len(user_help_keyboard.inline_keyboard)
    for i in range(outer_length):
        inner_length = len(user_help_keyboard.inline_keyboard[i])
        for j in range(inner_length):
            if user_help_keyboard.inline_keyboard[i][j]["text"] == input_data:
                user_help_keyboard.inline_keyboard[i][j] = InlineKeyboardButton(
                    emoji.emojize(input_data + ' :rocket: '),
                    callback_data=input_data)

                return user_help_keyboard
            if user_help_keyboard.inline_keyboard[i][j]["text"] == emoji.emojize(input_data + ' :rocket: '):
                user_help_keyboard.inline_keyboard[i][j] = InlineKeyboardButton(input_data, callback_data=input_data)
                return user_help_keyboard

    return user_help_keyboard


def confirm_location_keyboard():
    keyboard = [[InlineKeyboardButton('Confirm', callback_data='view_posts'),
                 InlineKeyboardButton('Type in New Location', callback_data='location')]]
    return InlineKeyboardMarkup(keyboard)


def get_location_keyboard_markup():
    location_keyboard = KeyboardButton(text="Send Live Location",
                                       request_location=True)  # creating location button object
    custom_keyboard = [[location_keyboard]]  # creating keyboard object
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    # ReplyKeyboardRemove(custom_keyboard, remove_keyboard=True)
    return reply_markup


def view_posts_keyboard():
    keyboard = [[InlineKeyboardButton('1',callback_data='1'),
                 InlineKeyboardButton('2',callback_data='2'),
                 InlineKeyboardButton('3',callback_data='3'),
                 InlineKeyboardButton('4',callback_data='4'),
                 InlineKeyboardButton('5',callback_data='5')],
                [InlineKeyboardButton('Create Post', callback_data='create_posts')]]
    return InlineKeyboardMarkup(keyboard)


def create_post_keyboard():
    keyboard = [[InlineKeyboardButton('Create Post', callback_data='create_posts')]]
    return InlineKeyboardMarkup(keyboard)
