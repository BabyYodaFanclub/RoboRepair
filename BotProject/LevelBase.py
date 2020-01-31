from abc import ABCMeta, abstractmethod

from State import State


class LevelBase(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def accept_text_message(self, chat_id: str, text: str, global_state: State):
        raise NotImplementedError

    @abstractmethod
    def accept_voice_message(self, chat_id: str, voice_message, global_state: State):
        raise NotImplementedError
