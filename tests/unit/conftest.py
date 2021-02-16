import abc
import random
from requests import exceptions
from collections import namedtuple
from typing import Optional, Callable

import pytest
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
)

from chatbot import main
from chatbot.app import fp_api_manager
from .conversation import (
    Conversation,
    UserAction,
    BotReply,
    Write,
    Click,
)
from .request_calls import GetCall, PostCall


@pytest.fixture()
def mock_bot(monkeypatch):
    monkeypatch.setattr(main, "check_telegram_token", lambda: None)

    updater = MockUpdater()
    monkeypatch.setattr(main, "Updater", updater)

    main.main()
    return MockBot(updater=updater)


@pytest.fixture()
def mock_requests(monkeypatch):
    mock_session = MockSession()
    mock_requests = MockRequests(mock_session)
    monkeypatch.setattr(fp_api_manager, "requests", mock_requests)
    return mock_session


class MockRequests:
    def __init__(self, mock_session):
        self._mock_session = mock_session

    def Session(self):
        return self._mock_session

    @property
    def exceptions(self):
        return exceptions


class MockSession:

    _GET_QUERY_TYPE = "GET"
    _POST_QUERY_TYPE = "GET"

    def __init__(self):
        self._upcoming_returns = {
            self._GET_QUERY_TYPE: [],
            self._POST_QUERY_TYPE: [],
        }
        self._handled_calls = []

    def __call__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        self._handled_calls.append(PostCall(*args, **kwargs))
        return self._get_return(self._POST_QUERY_TYPE)

    def get(self, *args, **kwargs):
        self._handled_calls.append(GetCall(*args, **kwargs))
        return self._get_return(self._GET_QUERY_TYPE)

    def add_upcoming_post_return(self, response, status_code=0):
        self._add_upcoming_return(self._POST_QUERY_TYPE, status_code, response)

    def add_upcoming_get_return(self, response, status_code=0):
        self._add_upcoming_return(self._GET_QUERY_TYPE, status_code, response)

    def _get_return(self, query_type):
        upcoming_returns = self._upcoming_returns[query_type]
        if len(upcoming_returns) > 0:
            return upcoming_returns.pop(0)
        else:
            raise RuntimeError("To use the mock session you need to define all the upcoming GET/POST returns.")

    def _add_upcoming_return(self, query_type, status_code, response):
        mock_response = MockResponse(response, status_code)
        self._upcoming_returns[query_type].append(mock_response)

    def assert_calls(self, calls):
        assert calls == self._handled_calls


class MockResponse:
    def __init__(self, response, status_code):
        self._response = response
        self._status_code = status_code

    def json(self):
        return self._response

    @property
    def status_code(self):
        return self._status_code


class MockBot:
    def __init__(self, updater):
        self._updater = updater
        self._updater.set_bot(self)
        self._dispatcher = updater._dispatcher
        self._dispatcher.set_bot(self)
        self._last_click_answered = False
        self.last_message: Optional[MockMessage] = None
        # TODO should this live here?
        self._chat_id = self._get_new_chat_id()

    def assert_conversation(self, conversation: Conversation):
        for action in conversation:
            if isinstance(action, UserAction):
                if isinstance(action.action, Write):
                    self.write_as_user(action.action.text)
                elif isinstance(action.action, Click):
                    self.click_as_user(action.action.button)
                else:
                    raise TypeError(f"Unknown action: {action.action}")
            elif isinstance(action, BotReply):
                text = self.get_text_of_last_message()
                buttons = self.get_buttons_of_last_message()
                assert text == action.text, f"{text} != {action.text}"
                assert buttons == action.buttons, f"{buttons} != {action.buttons}"
            else:
                raise TypeError(f"Unknown action: {action}")

    def write_as_user(self, message):
        self._dispatcher._handle_message(message)

    def click_as_user(self, button_text):
        self._last_click_answered = False
        callback_data = self._callback_data_from_button(button_text)
        self._dispatcher._handle_click(callback_data)

    def set_user_data_entry(self, key, value):
        user_data = self._get_user_data()
        user_data[key] = value

    def get_text_of_last_message(self):
        if self.last_message is None:
            return None
        return self.last_message['text']

    def get_buttons_of_last_message(self):
        inline_keyboard = self._last_inline_keyboard()
        if inline_keyboard is None:
            return None
        return [[entry['text'] for entry in row] for row in inline_keyboard]

    def send_message(self, **kwargs):
        self.last_message = MockMessage(self, **kwargs)

    def _callback_data_from_button(self, button_text):
        inline_keyboard = self._last_inline_keyboard()
        if inline_keyboard is None:
            return None
        for row in inline_keyboard:
            for entry in row:
                if entry['text'] == button_text:
                    return entry['callback_data']
        return None

    def _last_inline_keyboard(self):
        inline_keyboard_markup = self._last_inline_keyboard_markup()
        if inline_keyboard_markup is None:
            return None
        return inline_keyboard_markup['inline_keyboard']

    def _last_inline_keyboard_markup(self):
        if self.last_message is None:
            return None
        return self.last_message.get('reply_markup')

    def _get_new_chat_id(self):
        # TODO random for now
        return random.randint(0, 100)

    def _get_user_data(self):
        return self._dispatcher._context._user_data


class MockUpdater:
    def __call__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._dispatcher = MockDispatcher(self)
        self._bot = None
        return self

    @property
    def dispatcher(self):
        return self._dispatcher

    def set_bot(self, bot):
        self._bot = bot

    def start_polling(self):
        pass

    def idle(self):
        pass


class MockDispatcher:
    def __init__(self, updater):
        self._mock_handlers = []
        self._updater = updater
        self._context = MockContext()
        self._bot = None

    def set_bot(self, bot):
        self._bot = bot
        self._context.bot = bot

    def add_handler(self, handler):
        mock_handler = get_mock_handler(handler)
        self._mock_handlers.append(mock_handler)

    def _handle_message(self, message):
        return self._handle_user_action(_UserAction(message=message))

    def _handle_click(self, callback_data):
        return self._handle_user_action(_UserAction(callback_data=callback_data))

    def _handle_user_action(self, user_action):
        for mock_handler in self._mock_handlers:
            callback = mock_handler.callback(user_action)
            if callback is not None:
                update = MockUpdate(
                    self._bot,
                    text=user_action.message,
                    data=user_action.callback_data,
                )
                callback_return = callback(update, self._context)
                mock_handler.post_callback(callback_return)
                return True
        return False


user_actions = [
    "message",
    "callback_data",
]
_UserAction = namedtuple(
    "UserAction",
    user_actions,
    defaults=[None] * len(user_actions),
)


class MockContext:
    def __init__(self):
        self._user_data = {}
        self._bot = None

    @property
    def user_data(self):
        return self._user_data

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot


class MockMessage:
    def __init__(self, bot, **kwargs):
        self._bot = bot
        self._kwargs = kwargs

    def reply_text(self, **kwargs):
        self._bot.last_message = MockMessage(bot=self._bot, **kwargs)

    def __getitem__(self, key):
        return self._kwargs[key]

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError

    def get(self, key):
        return self._kwargs.get(key)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(" +
            ", ".join(f"{key}={value}" for key, value in self._kwargs.items()) +
            ')'
        )

    def __str__(self):
        to_return = f"{self.__class__.__name__}:\n"
        for key, value in self._kwargs.items():
            to_return += f"\t{key}: {value}\n"
        return to_return

    @property
    def chat_id(self):
        return self._bot._chat_id


class MockUpdate:
    def __init__(self, bot, text, data=None):
        self._message = MockMessage(bot, text=text)
        self._callback_query = MockCallbackQuery(
            bot=bot,
            message=self._message,
            data=data,
        )

    @property
    def message(self):
        return self._message

    @property
    def callback_query(self):
        return self._callback_query


class MockCallbackQuery:
    def __init__(self, bot, message, data):
        self._bot = bot
        self._message = message
        self._data = data

    def answer(self):
        self._bot.last_click_answered = True

    @property
    def message(self):
        return self._message

    @property
    def data(self):
        return self._data


def get_mock_handler(handler):
    if isinstance(handler, CommandHandler):
        return MockCommandHandler(handler)
    elif isinstance(handler, ConversationHandler):
        return MockConverstationHandler(handler)
    elif isinstance(handler, CallbackQueryHandler):
        return MockCallbackQueryHandler(handler)
    elif isinstance(handler, MessageHandler):
        return MockMessageHandler(handler)
    raise NotImplementedError(type(handler))


class BaseMockHandler(abc.ABC):
    @abc.abstractmethod
    def callback(self, user_action: _UserAction) -> Optional[Callable]:
        pass

    def post_callback(self, callback_return):
        pass


class MockCommandHandler(BaseMockHandler):
    def __init__(self, handler):
        assert isinstance(handler, CommandHandler)
        self._callback = handler.callback
        self._command = handler.command[0]

    def callback(self, user_action: _UserAction) -> Optional[Callable]:
        if not self._matches_command(user_action.message):
            return None
        return self._callback

    def _matches_command(self, message):
        cmd_prefix = '/'
        return message == f"{cmd_prefix}{self._command}"


class MockConverstationHandler(BaseMockHandler):
    def __init__(self, handler):
        self._entry_points = [get_mock_handler(h) for h in handler._entry_points]
        self._states = {state: [get_mock_handler(h) for h in handlers] for state, handlers in handler._states.items()}
        # None means here that the conversation handler is at the entry points
        self._current_state = None
        # TODO handle re-entry?

    def callback(self, user_action: _UserAction) -> Optional[Callable]:
        current_handlers = self._get_current_handlers()
        for handler in current_handlers:
            callback = handler.callback(user_action)
            if callback is not None:
                return callback
        return None

    def post_callback(self, callback_return):
        if callback_return == ConversationHandler.END:
            self._current_state = None
            return
        assert callback_return in self._states
        self._current_state = callback_return

    def _get_current_handlers(self):
        if self._current_state is None:
            return self._entry_points
        return self._states[self._current_state]


class MockCallbackQueryHandler(BaseMockHandler):
    def __init__(self, handler):
        self._callback = handler.callback
        self._pattern = handler.pattern

    def callback(self, user_action: _UserAction) -> Optional[Callable]:
        if not self._matches_button(user_action.callback_data):
            return None
        return self._callback

    def _matches_button(self, callback_data):
        if self._pattern is None:
            return True
        return bool(self._pattern.match(callback_data))


class MockMessageHandler(BaseMockHandler):
    def __init__(self, handler):
        self._callback = handler.callback
        self._filters = handler.filters

    def callback(self, user_action: _UserAction) -> Optional[Callable]:
        if not self._is_valid(user_action.message):
            return None
        return self._callback

    def _is_valid(self, message):
        # TODO should check if filters are correct
        return True
