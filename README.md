# FightPandemics-Telegram


### Running it locally 
1. Backend Setup: Since this app usages Setup backend service, first we need to setup the Docker.
For Docker Setup we follow the steps mentioned on 
https://github.com/FightPandemics/FightPandemics#docker-setup

2. Install Dependencies.

```bash
python setup.py develop
```

or if you have make

```bash
make install
```

3. Copy `token_data.default.yaml` to `token_data.yaml`.

4. Generate a chatbot token  and update `TELEGRAM_TOKEN` value in `token_data.yaml` file (the other constants below are only needed to run the tests)
   
   Follow the below steps which are already mentioned in the main.py file in the package.
 - Import logging library to connect and authenticate bot with Telegram API
 - To add functionalities first we need to define function then create handlers such as command handlers, message handlers and register it in the dispatcher. 
 As soon as we add new handlers to dispatcher, they are in effect.

```bash
 python chatbot/main.py
 ```
 
### Package Structure 

- main.py -> Chatbot entry point. This python module contains all start commands and all handlers
- handlers.py -> Contains function to define the chatbot response behavior 
- keyboards.py -> Keyboard Menus (Main menu, signed/unsigned user menu, help menu, etc.)
- fp_api_manager.py -> FightPandemics backend api manager
 
### Testing
We use both unit and end2end tests, see below.

#### Unit tests
The unit tests should test the logic of the chatbot without external dependencies.
This is done by mocking the actual telegram API and communication with the FP backend.
There is currently no official unit-testing framework for telegram chatbots compatible with the current telegram package.
There is [ptbtest](https://github.com/Eldinnie/ptbtest) however it only works with old version of the telegram package.

We therefore simply mock the telegram objects, see `tests/unit/conftest.py`.

To run the unit-tests simply do:
```bash
make tests
```
or without make
```bash
python3 -m pytest tests/unit
```

##### Coverage
When running the unit-tests through make, it will also print the test coverage of the current tests, i.e. how much of the code is actually tested.
To do this without make, run:
```bash
python3 -m pytest tests/unit --cov=chatbot --cov-report=term --cov-report=html
```
In both cases the coverage will be printed to the terminal and the folder `htmlcov` will be created.
To see an interactive view of which lines are tested and which are not, simply open `htmlcov/index.html`, i.e. by `open htmlcov/index.html` or `xdg-open htmlcov/index.html`.

#### End2end tests
The end2end tests checks the full behavior of the chatbot using a real conversation over the network etc.
These tests do not need to test all the logic of the chatbot, especially since they are slow and requires additional setup.
They only test that some basic features work to make sure that all setup and communication etc works.

To run the tests, take the following steps:

1. Create another bot, which will act as a test-client, talking to the actual chatbot.
   This will give you a new token, which you should fill in as `TEST_BOT_TOKEN` in `token_data.yaml`.
1. For the tests to be able to control your test bot you also need an API-token which you get setup [here](https://my.telegram.org/apps).
   This will give you both and ID and a hash which you should fill in as `API_ID` and `API_HASH` in `token_data.yaml`.
1. Make sure the chatbot and dependencies are installed and then run it
   ```bash
   python3 chatbot/main.py
   ```
   Leave it running, so open another terminal to run the actual tests.
1. To finally run the test, the easiest way is using [`make`](https://en.wikipedia.org/wiki/Make_(software)):
   ```bash
   make tests-end2end
   ```
   Alternatively you can directly do (this requires the test dependencies to already been installed):
   ```bash
   python3 -m pytest tests/end2end
   ```

### Linting
To check the linting of the code do:
```bash
make lint
```
or
```bash
python3 -m flake8 chatbot tests
```
