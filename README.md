# FightPandemics-Telegram


### Running it locally 
1. Backend Setup: Since this app usages Setup backend service, first we need to setup the Docker.
For Docker Setup we follow the steps mentioned on 
https://github.com/FightPandemics/FightPandemics#docker-setup

2. Install Dependenices and python-telegram-bot framework.

```{bash}
pip install python-telegram-bot
```

3. Generate a chatbot token  and update `TELEGRAM_TOKEN` value in app/constants.py file 
 - Import logging library to connect and authenticate bot with Telegram API
 - Update the `TELEGRAM_TOKEN` in the updater object in the main() function in main.py to start the bot.
 - To add functionalities first we need to define function then create handlers such as command handlers, message handlers and register it in the dispatcher. 
 As soon as we add new handlers to dispatcher, they are in effect.

 ```{bash}
python app/main.py
 ```
 
### Package Structure 

- main.py -> Chatbot entry point. This python module contains all start commands and all handlers
- handlers.py -> Contains function to define the chatbot response behavior 
- keyboards.py -> Keyboard Menus (Main menu, signed/unsigned user menu, help menu, etc.)
- fp_api_manager.py -> FightPandemics backend api manager
 
 