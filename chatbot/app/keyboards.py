from typing import List

import emoji
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from chatbot.app import patterns


CATEGORY_BUTTONS = [
    ["Medical Supplies", "Groceries/Food", "Business"],
    ["Education", "Legal", "Wellbeing/Mental"],
    ["Entertainment", "Information", "Funding"],
    ["R&D", "Tech", "Others"],
]
# Flatten grid
CATEGORIES = [b for row in CATEGORY_BUTTONS for b in row]

BASE_MAIN_MENU_BUTTONS = [
    [patterns.REQUEST_HELP, patterns.OFFER_HELP],
    [patterns.VIEW_MY_POSTS, patterns.VIEW_MY_PROFILE],
    [patterns.CREATE_POST, patterns.ABOUT_FIGHTPANDEMICS],
]


def _construct_inline_button(button_text: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=button_text,
        callback_data=button_text,
    )


def _construct_inline_keyboard(buttons: List[List[str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [_construct_inline_button(button_text) for button_text in row]
        for row in buttons
    ])


# define all keyboards here.
def request_or_offer():
    """keyboard to choose to request or offer help"""
    return _construct_inline_keyboard([[patterns.REQUEST_HELP, patterns.OFFER_HELP]])


def help_categories():
    """keyboard for choosing help categories"""
    buttons = CATEGORY_BUTTONS[:]
    buttons.append([patterns.DONE])
    return _construct_inline_keyboard(buttons)


def main_menu(is_user_signed_in: bool):
    return _construct_inline_keyboard(_main_menu_buttons(is_user_signed_in))


def _main_menu_buttons(is_user_signed_in: bool) -> List[List[str]]:
    buttons = BASE_MAIN_MENU_BUTTONS[:]
    if is_user_signed_in:
        buttons.append([patterns.SIGNOUT])
    else:
        buttons.append([patterns.LOGIN])
    return buttons


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
        _construct_inline_button(patterns.CREATE_POST),
        InlineKeyboardButton('Next > ', callback_data='display_selected_post_next'),
    ])
    return InlineKeyboardMarkup(grid)


def display_selected_post():
    _construct_inline_keyboard([[
        patterns.SEE_COMMENTS, patterns.VIEW_AUTHOR_PROFILE, patterns.POST_COMMENT
    ]])


def no_location():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('I don\'t want to share my location right now', callback_data='view_posts'),
    ]])


def confirm_location():
    return InlineKeyboardMarkup([[InlineKeyboardButton('Confirm', callback_data='view_posts')]])


def create_post():
    return _construct_inline_keyboard([[patterns.CREATE_POST]])
