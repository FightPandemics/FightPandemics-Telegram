from time import sleep
import pytest_bdd as bdd
bdd.scenarios('basic.feature')


@bdd.given('A conversation with the chatbot is open', target_fixture='client')
def setup_conversation(new_client):
    print("HELLO")
    return new_client


@bdd.when(bdd.parsers.parse('I write "{message}"'))
def user_writes_message(client, message):
    client.send_message(message)


@bdd.when(bdd.parsers.parse('I wait "{seconds}" seconds'))
def user_writes_message(client, seconds):
    sleep(float(seconds))


@bdd.then(bdd.parsers.parse('I should receive the new message "{exp_message}"'))
def assert_received_message(client, exp_message):
    msg = client.get_message()
    assert msg['text'] == process_message(exp_message)


@bdd.then(bdd.parsers.parse('I should see the buttons "{exp_buttons}"'))
def assert_buttons(client, exp_buttons):
    msg = client.get_message(next_msg=False)
    buttons = msg['reply_markup']['inline_keyboard'][0]
    button_texts = [b['text'] for b in buttons]
    for b, exp_b in zip(sorted(button_texts), exp_buttons.split(', ')):
        b == exp_b


def process_message(message):
    return message.replace('\\n', '\n')
