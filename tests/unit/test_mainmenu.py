def test_mainmenu(mock_bot):
    mock_bot.write_as_user("/mainmenu")

    print(mock_bot.last_message)

    expected_text = "This is FightPandemics Chatbot main menu, What would you like to do?"
    assert mock_bot.get_text_of_last_message() == expected_text

    expected_buttons = [
        ['Request Help', 'Offer Help'],
        ['View My Posts', 'View My Profile'],
        ['Create Post', 'About FightPandemics'],
        ['Login'],
    ]
    assert mock_bot.get_buttons_of_last_message() == expected_buttons
