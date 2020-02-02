from abc import abstractmethod, ABCMeta
import os

from BotBase import BotBase
from LevelBase import LevelBase
from Speech import Speech
from State import State

from ChatType import ChatType


class AbstractLevel(LevelBase, metaclass=ABCMeta):

    is_level_finished = False

    def current_dir(self):
        return os.path.dirname(os.path.realpath(self.get_file()))

    def __init__(self):
        self.message_sequence = None

    @abstractmethod
    def get_file(self):
        pass

    def accept_chat_start(self, bot: BotBase, chat_id: str, global_state: State) -> 'LevelBase':
        global_state.chat_id = chat_id
        return self.start(bot, global_state)

    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        global_state.chat_id = chat_id
        return self.resume(bot, global_state, ChatType.TEXT, text)

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        global_state.chat_id = chat_id

        speech = Speech()
        text = speech.speech_to_text(voice_message)

        return self.resume(bot, global_state, ChatType.VOICE, text)

    def start(self, bot: BotBase, global_state: State) -> 'LevelBase':
        return self

    def resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        if self.message_sequence is None:
            self.level_resume(bot, global_state, chat_type, message)
        else:
            self.message_sequence.resume(bot, global_state, chat_type, message)

        return self.end(global_state) if self.is_level_finished else self

    @abstractmethod
    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message) -> 'LevelBase':
        pass

    @abstractmethod
    def end(self, global_state: State) -> 'LevelBase':
        pass

    @abstractmethod
    def check_for_win(self, global_state: State):
        pass

    def set_level_completed(self):
        self.is_level_finished = True

    def end_message_sequence(self):
        self.message_sequence = None
