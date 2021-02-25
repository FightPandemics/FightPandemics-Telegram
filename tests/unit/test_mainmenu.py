from chatbot.app import keyboards

from .conversation import (
    UserAction,
    BotReply,
    Write,
)
from .login import login_user


def test_mainmenu_not_logged_in(mock_bot):
    buttons = keyboards._main_menu_buttons(is_user_signed_in=False)

    conversation = [
        UserAction(Write("/mainmenu")),
        BotReply(
            text="This is FightPandemics Chatbot main menu, What would you like to do?"
                 " To see more options, create posts etc you need to first login.",
            buttons=buttons,
        ),
    ]

    mock_bot.assert_conversation(conversation)


def test_mainmenu_logged_in(mock_bot):
    login_user(mock_bot)

    buttons = keyboards._main_menu_buttons(is_user_signed_in=True)

    conversation = [
        UserAction(Write("/mainmenu")),
        BotReply(
            text="This is FightPandemics Chatbot main menu, What would you like to do?",
            buttons=buttons,
        ),
    ]

    mock_bot.assert_conversation(conversation)
