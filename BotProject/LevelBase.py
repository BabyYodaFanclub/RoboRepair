from abc import ABCMeta, abstractmethod

from BotBase import BotBase
from State import State


class LevelBase(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        raise NotImplementedError

    @abstractmethod
    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        raise NotImplementedError
