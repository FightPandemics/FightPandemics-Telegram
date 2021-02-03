import emoji
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from chatbot.app.patterns import Pattern


CATEGORIES = [
    "Medical Supplies",
    "Groceries/Food",
    "Business",
    "Education",
    "Legal",
    "Wellbeing/Mental",
    "Entertainment",
    "Information",
    "Funding",
    "R&D",
    "Tech",
    "Others",
]


class Button:
    RequestHelp = InlineKeyboardButton('Request Help', callback_data=Pattern.REQUEST_HELP)
    OfferHelp = InlineKeyboardButton('Offer Help', callback_data=Pattern.REQUEST_HELP)
    Done = InlineKeyboardButton('Done', callback_data=Pattern.DONE)
    CreatePost = InlineKeyboardButton('Create Post', callback_data='create_post')


# define all keyboards here.
def request_or_offer():
    """keyboard to choose to request or offer help"""
    return InlineKeyboardMarkup([[Button.RequestHelp, Button.OfferHelp]])


def help_categories():
    """keyboard for choosing help categories"""
    buttons_per_row = 3
    grid = []
    row = []
    for i, category in enumerate(CATEGORIES):
        row.append(InlineKeyboardButton(
            category,
            callback_data=category,
        ))
        if (i + 1) % buttons_per_row == 0:
            grid.append(row)
            row = []
    if len(row) > 0:
        grid.append(row)
    grid.append([Button.Done])
    return InlineKeyboardMarkup(grid)


def main_menu(is_user_signed_in: bool):
    buttons = [
        [
            Button.RequestHelp,
            Button.OfferHelp,
        ],
        [
            InlineKeyboardButton('View My Posts', callback_data='view_my_posts'),
            InlineKeyboardButton('View My Profile', callback_data='view_my_profile'),
        ],
        [
            Button.CreatePost,
            InlineKeyboardButton('About FightPandemics', callback_data='about'),
        ],
    ]

    if is_user_signed_in:
        button_text = 'Signout'
    else:
        button_text = 'Login'
    callback_data = button_text.lower()
    buttons.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    return InlineKeyboardMarkup(buttons)


def checklist(keyboard, selected_buttons):
    for row in keyboard.inline_keyboard:
        for i, button in enumerate(row):
            current_text = button["text"]
            if current_text in selected_buttons:
                row[i] = InlineKeyboardButton(
                    emoji.emojize(current_text + ' :rocket: '),
                    callback_data=button["callback_data"],
                )
    return keyboard


def view_posts():
    numbers_per_line = 5
    total_numbers = 10
    grid = []
    row = []
    for n in range(1, total_numbers + 1):
        button = InlineKeyboardButton(str(n), callback_data=f'display_selected_post_{n}')
        row.append(button)
        if n % numbers_per_line == 0:
            grid.append(row)
            row = []
    if len(row) > 0:
        grid.append(row)

    grid.append([
        InlineKeyboardButton('< Prev', callback_data='display_selected_post_prev'),
        Button.CreatePost,
        InlineKeyboardButton('Next > ', callback_data='display_selected_post_next'),
    ])
    return InlineKeyboardMarkup(grid)


def display_selected_post():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('See Comments', callback_data='see_comments'),
        InlineKeyboardButton('View Author Profile', callback_data='view_author_profile'),
        InlineKeyboardButton('Post Comment', callback_data='post_comment')
    ]])


def no_location():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('I don\'t want to share my location right now', callback_data='view_posts'),
    ]])


def confirm_location():
    return InlineKeyboardMarkup([[InlineKeyboardButton('Confirm', callback_data='view_posts')]])


def create_post():
    return InlineKeyboardMarkup([[Button.CreatePost]])
