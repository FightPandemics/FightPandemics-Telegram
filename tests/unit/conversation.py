from dataclasses import dataclass
from typing import List, Union, Optional


@dataclass
class Click:
    button: str


@dataclass
class Write:
    text: str


@dataclass
class UserAction:
    action: Union[Write, Click]


@dataclass
class BotReply:
    text: Optional[str]
    buttons: Optional[List[List[str]]]


Conversation = List[Union[UserAction, BotReply]]
