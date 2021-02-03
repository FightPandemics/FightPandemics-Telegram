import os
import sys
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


PATH_TO_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_TO_TOKEN_FILE = os.path.join(PATH_TO_HERE, "..", "..", "token_data.yaml")


def load_token_file_data():
    with open(PATH_TO_TOKEN_FILE) as f:
        data = load(f, Loader=Loader)
    return data


token_data = load_token_file_data()
FP_BASE_URL = token_data["FP_BASE_URL"]
TELEGRAM_TOKEN = token_data["TELEGRAM_TOKEN"]

# For running tests
CHATBOT_NAME = token_data["CHATBOT_NAME"]
API_ID = token_data["API_ID"]
API_HASH = token_data["API_HASH"]
TEST_BOT_TOKEN = token_data["TEST_BOT_TOKEN"]


def _check_token():
    names = ["FP Base URL", "Telegram token"]
    values = [FP_BASE_URL, TELEGRAM_TOKEN]
    _check_constants(names, values)
    assert len(TELEGRAM_TOKEN) > 0, "no telegram token"


def _check_test_constants():
    names = ["API ID", "API Hash", "Chat bot name", "Test bot token"]
    values = [API_ID, API_HASH, CHATBOT_NAME, TEST_BOT_TOKEN]
    _check_constants(names, values)


def _check_constants(names, values):
    for (name, value) in zip(names, values):
        assert len(value) > 0, f"no {name}"


if __name__ == '__main__':
    _check_token()
    TEST_FLAG = '--check-test-constants'
    if TEST_FLAG in sys.argv:
        _check_test_constants()
        sys.argv.remove(TEST_FLAG)
    if len(sys.argv) != 1:
        raise ValueError(f"Unknown flag {sys.argv[1:]}")
