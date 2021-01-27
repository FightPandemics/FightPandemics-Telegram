TEST_DIR         = tests
SOURCE_DIR       = chatbot
CONSTANTS_FILE   = ${SOURCE_DIR}/app/constants.py
CLIENT_TEST_FILE = ${TEST_DIR}/end2end/fixtures/client.py

help:
	@echo "install    Install required packages and chatbot"
	@echo "test-deps  Install required packages to run tests"
	@echo "tests      Run tests"
	@echo "lint       Run linter"

install:
	@python3 -m pip install -r requirements.txt
	@python3 -m pip install -e .

test-deps:
	@python3 -m pip install -r test_requirements.txt

tests: _check_constants test-deps _setup_test_client
	@pytest ${TEST_DIR}

_setup_test_client:
	@python3 ${CLIENT_TEST_FILE}

_check_constants:
	@python3 ${CONSTANTS_FILE} --check-test-constants

lint:
	@python3 -m flake8 ${SOURCE_DIR} ${TEST_DIR}
