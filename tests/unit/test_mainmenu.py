from .conversation import (
    UserAction,
    BotReply,
    Write,
)


def test_mainmenu(mock_bot):
    conversation = [
        UserAction(Write("/mainmenu")),
        BotReply(
            text="This is FightPandemics Chatbot main menu, What would you like to do?",
            buttons=[
                ['Request Help', 'Offer Help'],
                ['View My Posts', 'View My Profile'],
                ['Create Post', 'About FightPandemics'],
                ['Login'],
            ]
        ),
    ]

    mock_bot.assert_conversation(conversation)
