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

3. Generate a chatbot token  and update `TELEGRAM_TOKEN` value in `chatbot/app/constants.py` file (the other constants below are only needed to run the tests)
   
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
To run the tests, take the following steps:

1. Create another bot, which will act as a test-client, talking to the actual chatbot.
   This will give you a new token, which you should fill in as `TEST_BOT_TOKEN` in `chatbot/app/constants.py`.
1. For the tests to be able to control your test bot you also need an API-token which you get setup [here](https://my.telegram.org/apps).
   This will give you both and ID and a hash which you should fill in as `API_ID` and `API_HASH` in `chatbot/app/constants.py`.
1. Make sure the chatbot and dependencies are installed and then run it
   ```bash
   python3 chatbot/main.py
   ```
   Leave it running, so open another terminal to run the actual tests.
1. To finally run the test, the easiest way is using [`make`](https://en.wikipedia.org/wiki/Make_(software)):
   ```bash
   make tests
   ```
   Alternatively you can directly do (this requires the test dependencies to already been installed):
   ```bash
   python3 -m pytest tests
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
