import os
from timeit import default_timer as timer

import pytest
from pyrogram import Client

from chatbot.app.constants import API_ID, API_HASH, CHATBOT_NAME, TEST_BOT_TOKEN


PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))


class BotClient():
    def __init__(self, bot_name, app):
        self._bot_name = bot_name
        self._app = app
        self._last_message_id = None

    def send_message(self, message, delay=0):
        msg = self._app.send_message(self._bot_name, message)
        self._last_message_id = msg.message_id

    def get_message(self):
        return self._app.get_messages(self._bot_name, self._last_message_id)

    def wait_for_next_message(self, delay_between_checks=0.1, timeout=2):
        start_time = timer()
        while True:
            msg = self._app.get_messages(self._bot_name, self._last_message_id + 1)
            if not msg.empty:
                self._last_message_id += 1
                break
            current_time = timer()
            elapsed_time = current_time - start_time
            if elapsed_time > timeout:
                raise TimeoutError("Waiting for next messages timed out")

    def click_button(self, button_label):
        button_id = self._get_button_id(button_label)
        msg = self.get_message()
        msg.click(*button_id)

    def _get_button_id(self, button_label):
        for i, row in enumerate(self.get_current_button_labels()):
            for j, b in enumerate(row):
                if b == button_label:
                    return j, i
        raise ValueError(f"No such button with label {button_label}")

    def get_current_button_labels(self):
        msg = self.get_message()
        button_rows = msg['reply_markup']['inline_keyboard']
        button_labels = [[b['text'] for b in buttons] for buttons in button_rows]
        return button_labels

    def stop(self):
        self._app.stop()


def setup_new_client():
    app = Client(
        "test_client",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=TEST_BOT_TOKEN,
        workdir=PATH_TO_HERE,
    )
    app.start()
    return BotClient(
        bot_name=CHATBOT_NAME,
        app=app,
    )


@pytest.fixture
def new_client():
    client = setup_new_client()
    yield client
    client.stop()


if __name__ == '__main__':
    setup_new_client()
