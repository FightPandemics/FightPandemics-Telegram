# FightPandemics-Telegram


### Running it locally 
1. Backend Setup: Since this app usages Setup backend service, first we need to setup the Docker.
For Docker Setup we follow the steps mentioned on 
https://github.com/FightPandemics/FightPandemics#docker-setup

2. Install Dependencies.

```{bash}
python setup.py develop
```

or if you have make

```bash
make install
```

3. Generate a chatbot token  and update `TELEGRAM_TOKEN` value in chatbot/app/constants.py file (the other constants below are only needed to run the tests)
   
   Follow the below steps which are already mentioned in the main.py file in the package.
 - Import logging library to connect and authenticate bot with Telegram API
 - To add functionalities first we need to define function then create handlers such as command handlers, message handlers and register it in the dispatcher. 
 As soon as we add new handlers to dispatcher, they are in effect.

```{bash}
 python chatbot/main.py
 ```
 
### Package Structure 

- main.py -> Chatbot entry point. This python module contains all start commands and all handlers
- handlers.py -> Contains function to define the chatbot response behavior 
- keyboards.py -> Keyboard Menus (Main menu, signed/unsigned user menu, help menu, etc.)
- fp_api_manager.py -> FightPandemics backend api manager
 
### Testing
To run the tests, update `API_ID`, `API_HASH` and `CHATBOT_NAME` in `chatbot/app/constants.py`. The API token you get by setting up an app to use for testing [here](https://my.telegram.org/apps).

To run the test, first make sure you installed the chatbot and dependencies, see above.
Then using [`make`](https://en.wikipedia.org/wiki/Make_(software)), simply do:
```bash
make tests
```

The first time you run the test you will need to input your phone number and a confirmation code. This will create a file `tests/end2end/fixtures/test_client.session` which you should keep secure. If you delete the file you will need to input the phone number and confirmation code again.

### Linting
To check the linting of the code do:
```bash
make lint
```
