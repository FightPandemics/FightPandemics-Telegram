from time import sleep
import pytest_bdd as bdd
bdd.scenarios('basic.feature')


@bdd.given('A conversation with the chatbot is open', target_fixture='client')
def setup_conversation(new_client):
    return new_client


@bdd.when(bdd.parsers.parse('I write "{message}"'))
def write_message(client, message):
    client.send_message(message)


@bdd.when('I wait for the next message')
def wait_for_message(client):
    client.wait_for_next_message()


@bdd.when(bdd.parsers.parse('I click the button "{button}"'))
def click_button(client, button):
    client.click_button(button)


@bdd.then(bdd.parsers.parse('I should receive the new message "{exp_message}"'))
def assert_received_message(client, exp_message):
    msg = client.get_message()
    assert msg['text'] == process_string_with_linebreaks(exp_message)


@bdd.then(bdd.parsers.parse('I should see the buttons "{exp_buttons}"'))
def assert_buttons(client, exp_buttons):
    exp_rows = process_expected_buttons(exp_buttons)
    button_rows = client.get_current_button_labels()
    print(exp_buttons)
    print(button_rows)
    for row, exp_row in zip(button_rows, exp_rows):
        for button, exp_button in zip(row, exp_row):
            assert button == exp_button


def process_string_with_linebreaks(message):
    return message.replace('\\n', '\n')


def process_expected_buttons(exp_buttons):
    rows = []
    for expected_row in process_string_with_linebreaks(exp_buttons).split('\n'):
        row = []
        for button in expected_row.split(','):
            row.append(button.strip())
        rows.append(row)
    return rows
