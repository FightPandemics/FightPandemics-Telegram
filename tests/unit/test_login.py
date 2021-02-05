import random

from chatbot.app import keyboards
from chatbot.app.fp_api_manager import VALID_STATUS_CODE

from .conversation import (
    UserAction,
    BotReply,
    Write,
    Click,
)


def test_correct_login(mock_bot, mock_requests):
    # Mock request response for correct login
    user_id = random.randint(0, 100)
    token = random.randint(0, 100)
    mock_requests.add_upcoming_post_return(
        response={
            'emailVerified': True,
            'user': {'id': user_id},
            'token': token,
        },
        status_code=VALID_STATUS_CODE,
    )

    # Login conversation
    username = "Test Name"
    password = "test_password"
    conversation = [
        UserAction(Write("/mainmenu")),
        UserAction(Click("Login")),
        BotReply(text="Please provide your username:"),
        UserAction(Write(username)),
        BotReply(text=f"Please enter password for username \"{username}\":"),
        UserAction(Write(password)),
        BotReply(
            text="Login Successful. What would you like to do?",
            buttons=keyboards._main_menu_buttons(is_user_signed_in=True),
        ),
    ]

    mock_bot.assert_conversation(conversation)


def test_incorrect_login(mock_bot, mock_requests):
    # Response with no entries implying incorrect login
    mock_requests.add_upcoming_post_return(response={}, status_code=VALID_STATUS_CODE)

    username = "Test Name"
    password = "test_password"

    conversation = [
        UserAction(Write("/mainmenu")),
        UserAction(Click("Login")),
        UserAction(Write(username)),
        UserAction(Write(password)),
        BotReply(
            text="Incorrect username, password combination. Please try to login again",
            buttons=keyboards._main_menu_buttons(is_user_signed_in=False),
        )
    ]

    mock_bot.assert_conversation(conversation)
