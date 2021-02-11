from .conversation import (
    UserAction,
    BotReply,
    Write,
)


from chatbot.app import keyboards, patterns


def test_mainmenu(mock_bot):
    buttons = keyboards.BASE_MAIN_MENU_BUTTONS[:]
    buttons.append([patterns.LOGIN])

    conversation = [
        UserAction(Write("/mainmenu")),
        BotReply(
            text="This is FightPandemics Chatbot main menu, What would you like to do?",
            buttons=buttons,
        ),
    ]

    mock_bot.assert_conversation(conversation)
