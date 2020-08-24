from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# define all keyboards here.

def welcome_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Request Help', callback_data='request_help')],
               [InlineKeyboardButton('Offer Help', callback_data='offer_help')]]
    return InlineKeyboardMarkup(keyboard)


def login_keyboard():
    #fp_login_url = LoginUrl(url="https://fightpandemics.com")
    keyboard = [[InlineKeyboardButton('UserName',
                                      switch_inline_query_current_chat="UserName")]]
    return InlineKeyboardMarkup(keyboard)


def help_keyboard():
    keyboard = [[InlineKeyboardButton('Medical Help', callback_data='medical_help')],
                [InlineKeyboardButton('Other Help', callback_data='other_help')],
                [InlineKeyboardButton('Go to Main Menu', callback_data='main_menu')]]
    return InlineKeyboardMarkup(keyboard)


def other_help_keyboard():
    keyboard = [[InlineKeyboardButton('Groceries/food', callback_data='Groceries/food')],
                [InlineKeyboardButton('Medical Supplies', callback_data='Medical Supplies')],
                [InlineKeyboardButton('Funding/Donate', callback_data='Funding/Donate')],
                [InlineKeyboardButton('Well-being/Mental', callback_data='Well-being/Mental')],
                [InlineKeyboardButton('Information', callback_data='Information')],
                [InlineKeyboardButton('Technology', callback_data='Technology')],
                [InlineKeyboardButton('Legal', callback_data='Legal')],
                [InlineKeyboardButton('Education', callback_data='Education')],
                [InlineKeyboardButton('Business', callback_data='Business')]
        ]
    return InlineKeyboardMarkup(keyboard)


def signed_user_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Restart Offer Help', callback_data='offer_help')],
                [InlineKeyboardButton('Restart Request Help', callback_data='request_help')],
                [InlineKeyboardButton('View My Posts', callback_data='view_posts')],
                [InlineKeyboardButton('View My Profile', callback_data='view_profile')],
                [InlineKeyboardButton('Signout', callback_data='signout')],
                [InlineKeyboardButton('About FightPandemics', callback_data='about')]]
    return InlineKeyboardMarkup(keyboard)


def unsinged_user_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Restart Offer Help', callback_data='offer_help')],
                [InlineKeyboardButton('Restart Request Help', callback_data='request_help')],
                [InlineKeyboardButton('View My Posts', callback_data='view_posts')],
                [InlineKeyboardButton('View My Profile', callback_data='view_profile')],
                [InlineKeyboardButton('Login/Signup', callback_data='login')],
                [InlineKeyboardButton('About FightPandemics', callback_data='about')]]
    return InlineKeyboardMarkup(keyboard)

