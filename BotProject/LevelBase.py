from abc import ABCMeta, abstractmethod

from Bot import Bot
from State import State


class LevelBase(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def accept_text_message(self, bot: Bot, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        raise NotImplementedError

    @abstractmethod
    def accept_voice_message(self, bot: Bot, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        raise NotImplementedError
