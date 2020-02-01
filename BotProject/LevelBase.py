import re
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

    def accept_chat_start(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        pass

    @staticmethod
    def extract_line_params(param_string: str) -> dict:
        out = {}
        matches = re.findall(r'\[([\w])(?:=((?:[\w\d]+,)*[\w\d]+))?\]', param_string)
        for match in matches:
            if len(match) > 1 and len(match[1]) >= 1:
                out[match[0]] = match[1].split(',')
            else:
                out[match[0]] = None

        return out
