import pytest

from .conversation import (
    UserAction,
    Write,
    Click,
)
from .login import login_user


def test_status_code(mock_bot, mock_requests):
    login_user(mock_bot)

    mock_requests.add_upcoming_get_return(response={}, status_code=0)

    conversation = [
        UserAction(Write("/mainmenu")),
        UserAction(Click("View My Posts")),
    ]

    with pytest.raises(ConnectionError) as err:
        mock_bot.assert_conversation(conversation)
    assert str(err.value) == "Could not get posts"
