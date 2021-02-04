def test_create_post(mock_bot):
    mock_bot.write_as_user("/mainmenu")
    mock_bot.click_as_user("Create Post")

    print(mock_bot.last_message)

    expected_text = "Do you want to make a post to Offer Help or Request Help?"
    assert mock_bot.get_text_of_last_message() == expected_text

    expected_buttons = [
        ['Request Help', 'Offer Help'],
    ]
    assert mock_bot.get_buttons_of_last_message() == expected_buttons

    mock_bot.click_as_user("Offer Help")

    print(mock_bot.last_message)

    expected_text = "What type of help would you like to offer? Please choose all the relevant tags and click done"
    assert mock_bot.get_text_of_last_message() == expected_text

    expected_buttons = [
        ['Medical Supplies', 'Groceries/Food', 'Business'],
        ['Education', 'Legal', 'Wellbeing/Mental'],
        ['Entertainment', 'Information', 'Funding'],
        ['R&D', 'Tech', 'Others'],
        ['Done'],
    ]
    assert mock_bot.get_buttons_of_last_message() == expected_buttons
