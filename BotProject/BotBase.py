from abc import ABCMeta, abstractmethod
from datetime import timedelta

from telegram import ChatAction


class BotBase(metaclass=ABCMeta):
    @abstractmethod
    def send_text(self, chat_id: str, text: str):
        pass

    @abstractmethod
    def send_image(self, chat_id: str, image: str):
        pass

    @abstractmethod
    def send_voice_message(self, chat_id: str, voice_message: str):
        pass

    @abstractmethod
    def send_chat_action(self, chat_id: str, action: ChatAction):
        pass

    @abstractmethod
    def schedule_message(self, chat_id: str, text: str, delay):
        pass

    @abstractmethod
    def delayed_type_message(self, chat_id: str, text: str, time_per_word: timedelta):
        pass
