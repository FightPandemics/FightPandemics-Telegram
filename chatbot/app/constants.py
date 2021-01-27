import sys

# Base URL
FP_BASE_URL = "http://127.0.0.1:8000/api/"

#################
# Access tokens #
########################################
# You get this when setting up the bot #
########################################
TELEGRAM_TOKEN = ""

########################################
# NOTE: BELOW IS ONLY NEEDED FOR TESTS #
########################################

#############
# API Token #
##################################################
# Create a token at https://my.telegram.org/apps #
# and fill in here                               #
##################################################
API_ID = ""
API_HASH = ""

#################
# Chat bot name #
##########################################
# Fill in the name you gave your chatbot #
##########################################
CHATBOT_NAME = ""


def _check_token():
    assert len(TELEGRAM_TOKEN) > 0, "no telegram token"


def _check_test_constants():
    for (name, t) in zip(["API ID", "API Hash", "Chat bot name"], [API_ID, API_HASH, CHATBOT_NAME]):
        assert len(t) > 0, f"no {name}"


if __name__ == '__main__':
    _check_token()
    TEST_FLAG = '--check-test-constants'
    if TEST_FLAG in sys.argv:
        _check_test_constants()
        sys.argv.remove(TEST_FLAG)
    if len(sys.argv) != 1:
        raise ValueError(f"Unknown flag {sys.argv[1:]}")
