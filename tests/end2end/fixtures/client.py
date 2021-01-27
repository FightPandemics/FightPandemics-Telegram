import os
import pytest
from pyrogram import Client
from chatbot.app.constants import API_ID, API_HASH, CHATBOT_NAME


PATH_TO_HERE = os.path.dirname(os.path.abspath(__file__))


class BotClient():
    def __init__(self, bot_name, app):
        self._bot_name = bot_name
        self._app = app
        self._last_message_id = None

    def send_message(self, message, delay=0):
        msg = self._app.send_message(self._bot_name, message)
        self._last_message_id = msg.message_id

    def get_message(self, delay=0, next_msg=True):
        if next_msg:
            self._last_message_id += 1
        return self._app.get_messages(self._bot_name, self._last_message_id)


def setup_new_client():
    app = Client(
        "test_client",
        api_id=API_ID,
        api_hash=API_HASH,
        workdir=PATH_TO_HERE,
    )
    app.start()
    return BotClient(
        bot_name=CHATBOT_NAME,
        app=app,
    )


@pytest.fixture
def new_client():
    yield setup_new_client()


if __name__ == '__main__':
    setup_new_client()
