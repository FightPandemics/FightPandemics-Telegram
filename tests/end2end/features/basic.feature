Feature: Test basic behaviour of app

    Scenario: Start
        Given A conversation with the chatbot is open
        When I write "/start"
        And I wait "1" seconds
        Then I should receive the new message "Hi! Welcome!\nWe are FightPandemics.\nA place to offer and request help.\nPandemics will continue to happen.\nWe help communities prepare and respond.\nWhat would you like to do?"
        And I should see the buttons "Request Help, Offer help"
