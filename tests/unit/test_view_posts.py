import pytest

from chatbot.app import keyboards, user_data
from chatbot.app.fp_api_manager import VALID_STATUS_CODES
from .conversation import (
    UserAction,
    BotReply,
    Write,
    Click,
)
from .login import login_user


TEST_POST_DATA = {
    '_id': 0,
    user_data.POST_TITLE: 'Test Post',
    user_data.AUTHOR: {
        user_data.AUTHOR_NAME: 'Test Name',
        user_data.LOCATION: {
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
        },
    },
    user_data.POST_CATEGORIES: ['category1'],
    user_data.POST_DESCRIPTION: "This is my test post",
    user_data.NUM_COMMENTS: 10,
}

EXPECTED_RESPONSE_HEADER = "Page {page_nr} of your posts\n\n"
EXPECTED_RESPONSE_BODY = """{post_nr}.  Test Post

By Test Name - Test City, Test State, Test Country

category1

This is my test post

10 Comments
"""


def _view_posts_buttons():
    inline_keyboard = keyboards.view_posts()['inline_keyboard']
    return [[b.text for b in row] for row in inline_keyboard]


def _get_expected_reply(num_posts):
    # TODO handle multiple pages
    expected_reply = EXPECTED_RESPONSE_HEADER.format(page_nr=1)
    for i in range(1, num_posts + 1):
        expected_reply += EXPECTED_RESPONSE_BODY.format(post_nr=i)
    return expected_reply


@pytest.mark.parametrize('num_posts', [1, 3])
def test_view_my_posts(mock_bot, mock_requests, num_posts):
    login_user(mock_bot)

    mock_requests.add_upcoming_post_return(
        response=[TEST_POST_DATA] * num_posts,
        status_code=VALID_STATUS_CODES[0],
    )

    conversation = [
        UserAction(Write("/mainmenu")),
        UserAction(Click("View My Posts")),
        BotReply(
            text=_get_expected_reply(num_posts=num_posts),
            buttons=_view_posts_buttons(),
        ),
    ]

    mock_bot.assert_conversation(conversation)
