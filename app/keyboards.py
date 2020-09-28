from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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


def keyboard_checklist(help_keyboard, input_data):
    outer_length = len(help_keyboard["inline_keyboard"])
    for i in range(outer_length):
        inner_length = len(help_keyboard["inline_keyboard"][i])
        for j in range(inner_length):
            if help_keyboard["inline_keyboard"][i][j]["text"] == input_data:
                help_keyboard["inline_keyboard"][i][j] = InlineKeyboardButton(
                    emoji.emojize(input_data + ' :thumbs_up:'),
                    callback_data=input_data)

                return help_keyboard
            if help_keyboard["inline_keyboard"][i][j]["text"] == emoji.emojize(input_data + ' :thumbs_up:'):
                help_keyboard["inline_keyboard"][i][j] = InlineKeyboardButton(input_data, callback_data=input_data)
                return help_keyboard

    return help_keyboard


# can be used later
# def help_keyboard():
#     keyboard = [[InlineKeyboardButton('Medical Help', callback_data='medical_help')],
#                 [InlineKeyboardButton('Other Help', callback_data='other_help')],
#                 [InlineKeyboardButton('Go to Main Menu', callback_data='main_menu')]]
#     return InlineKeyboardMarkup(keyboard)


