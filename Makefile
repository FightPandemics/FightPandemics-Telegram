SOURCE_DIR       = chatbot
MAIN             = ${SOURCE_DIR}/main.py
CONSTANTS_FILE   = ${SOURCE_DIR}/app/constants.py
TEST_DIR         = tests
UNIT_TESTS       = ${TEST_DIR}/unit
END2END_TESTS    = ${TEST_DIR}/end2end
CLIENT_TEST_FILE = ${TEST_DIR}/end2end/fixtures/client.py

help:
	@echo "install    Install required packages and chatbot"
	@echo "test-deps  Install required packages to run tests"
	@echo "tests      Run tests"
	@echo "lint       Run linter"

install: test-deps
	@python3 -m pip install -r requirements.txt
	@python3 -m pip install -e .

test-deps:
	@python3 -m pip install -r test_requirements.txt

tests:
	@python3 -m pytest ${UNIT_TESTS} --cov=${SOURCE_DIR} --cov-report=html --cov-report=term

tests-end2end: _check_constants _setup_test_client
	@python3 -m pytest ${END2END_TESTS}

lint:
	@python3 -m flake8 ${SOURCE_DIR} ${TEST_DIR}

_check_constants:
	@python3 ${CONSTANTS_FILE} --check-test-constants

_setup_test_client:
	@python3 ${CLIENT_TEST_FILE}


.PHONY: help install test-deps tests tests-end2end _run_bot _check_constants _setup_test_client lint
