from abc import abstractmethod, ABCMeta
import os

from BotBase import BotBase
from DialogActions import ImmediateNextAction
from LevelBase import LevelBase
from MessageSequence import MessageSequence
from Speech import Speech
from State import State

from ChatType import ChatType


class AbstractLevel(LevelBase, metaclass=ABCMeta):

    is_level_finished: bool
    valid_keys: dict
    message_sequence: MessageSequence

    def current_dir(self):
        return os.path.dirname(os.path.realpath(self.get_file()))

    def __init__(self):
        self.message_sequence = None
        self.is_level_finished = False
        self.valid_keys = {}

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

    def resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message) -> 'LevelBase':

        if not self.is_level_finished:
            if self.message_sequence is None:
                self.level_resume(bot, global_state, chat_type, message)
            else:
                self.message_sequence.resume(bot, global_state, chat_type, message)

        return self.end(global_state) if self.is_level_finished else self

    @staticmethod
    def __check_invariant(message, variants) -> bool:
        for var in variants:
            if var in message:
                return True

        return False

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        message = message.lower()

        for active, variants, callback in self.valid_keys.values():
            if not self.__check_invariant(message, variants):
                continue

            if not active:
                ImmediateNextAction.static_send(bot, global_state, 'Not at the moment')
            else:
                callback(bot, global_state)

            return

        ImmediateNextAction.static_send_error(bot, global_state)

    @abstractmethod
    def end(self, global_state: State) -> 'LevelBase':
        pass

    def set_level_completed(self):
        self.is_level_finished = True

    def end_level(self, bot: BotBase, global_state: State):
        self.set_level_completed()
        self.resume(bot, global_state, '', None)

    def run_message_sequence(self, bot: BotBase, global_state: State, name: str, callback: callable = None):
        if callback is None:
            callback = self.end_message_sequence

        self.set_message_sequence(name, lambda: callback(bot, global_state))
        self.start_message_sequence(bot, global_state)

    def set_message_sequence(self, name: str, end_callback: callable = None):
        if end_callback is None:
            end_callback = self.end_message_sequence

        self.message_sequence = MessageSequence(self.current_dir(), name, end_callback)

    def start_message_sequence(self, bot: BotBase, global_state: State):
        self.message_sequence.start(bot, global_state)

    def end_message_sequence(self, *x):
        self.message_sequence = None

