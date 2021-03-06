from abc import ABCMeta, abstractmethod

from telegram import ChatAction


class BotBase(metaclass=ABCMeta):
    @abstractmethod
    def send_text(self, chat_id: str, text: str):
        pass

    @abstractmethod
    def send_image(self, chat_id: str, image):
        pass

    @abstractmethod
    def send_voice_message(self, chat_id: str, voice_message):
        pass

    @abstractmethod
    def send_chat_action(self, chat_id: str, action: ChatAction):
        pass

    @abstractmethod
    def schedule_message(self, chat_id: str, text: str, delay, callback):
        pass

    @abstractmethod
    def delayed_type_message(self, chat_id: str, text: str, callback):
        pass

    @abstractmethod
    def send_iteratively_edited_message(self, chat_id: str, texts: list):
        pass
