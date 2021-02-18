import pytest

from chatbot.app import keyboards
from chatbot.app.handlers.create_post import _format_preview_from_data

from .conversation import (
    UserAction,
    BotReply,
    Write,
    Click,
)
from .login import login_user


def test_create_post_not_logged_in(mock_bot):
    conversation = [
        UserAction(Write("/mainmenu")),
        UserAction(Click("Offer Help")),
        BotReply(
            text="Please sign in to create a post",
            buttons=keyboards._main_menu_buttons(is_user_signed_in=False),
        ),
    ]

    mock_bot.assert_conversation(conversation)


@pytest.mark.parametrize('user_name', ['User Name', 'Other Name'])
@pytest.mark.parametrize('post_title', ['Some title', 'Other title'])
@pytest.mark.parametrize('post_description', ['Some description', 'Other description'])
@pytest.mark.parametrize('post_category', keyboards.CATEGORIES)
@pytest.mark.parametrize('duration', keyboards._duration_buttons()[0])
def test_create_post(
    mock_bot,
    user_name,
    post_title,
    post_description,
    post_category,
    duration,
):
    login_user(mock_bot, user_name=user_name)

    conversation = [
        UserAction(Write("/mainmenu")),
        UserAction(Click("Offer Help")),
        BotReply(
            text="What is the title of your post? (60 characters or less)",
        ),
        UserAction(Write(post_title)),
        BotReply(
            text="What is the description of your post?",
        ),
        UserAction(Write(post_description)),
        BotReply(
            text="What type of help would you like to offer? Please choose all the relevant tags and click done",
            buttons=keyboards._help_categories_buttons(),
        ),
        UserAction(Click(post_category)),
        UserAction(Click("Done")),
        BotReply(
            text=(
                "Please let us know your location so we can show the posts of your area! "
                "Either type in your address manually or share it using the 📎 below. "
                "If you don't want to share your location, click the button below."
            ),
            buttons=[["I don't want to share my location right now"]],
        ),
        UserAction(Click("I don't want to share my location right now")),
        BotReply(
            text="No location given, is this correct?",
            buttons=[["Confirm"]],
        ),
        UserAction(Click("Confirm")),
        BotReply(
            text="Since you have not specific a location this post will be shown worldwide.",
            buttons=[["Continue"]],
        ),
        UserAction(Click("Continue")),
        BotReply(
            text="What is the duration of your post?",
            buttons=keyboards._duration_buttons(),
        ),
        UserAction(Click(duration)),
        BotReply(
            text="Press preview to preview your post",
            buttons=[["Preview"]],
        ),
        UserAction(Click("Preview")),
        BotReply(
            text=_format_preview_from_data(
                title=post_title,
                content=post_description,
                categories=[post_category],
                user_name=user_name,
            ) + '\n\nTODO rest of conversation not implemented yet',
        ),
        # TODO continue when full conversation implemented
    ]

    mock_bot.assert_conversation(conversation)
