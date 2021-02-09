from .conversation import (
    UserAction,
    BotReply,
    Write,
    Click,
)


def test_create_post(mock_bot):
    conversation = [
        UserAction(Write("/mainmenu")),
        UserAction(Click("Create Post")),
        BotReply(
            text="Do you want to make a post to Offer Help or Request Help?",
            buttons=[['Request Help', 'Offer Help']]
        ),
        UserAction(Click("Offer Help")),
        BotReply(
            text="What type of help would you like to offer? Please choose all the relevant tags and click done",
            buttons=[
                ['Medical Supplies', 'Groceries/Food', 'Business'],
                ['Education', 'Legal', 'Wellbeing/Mental'],
                ['Entertainment', 'Information', 'Funding'],
                ['R&D', 'Tech', 'Others'],
                ['Done'],
            ]
        ),
    ]

    mock_bot.assert_conversation(conversation)
