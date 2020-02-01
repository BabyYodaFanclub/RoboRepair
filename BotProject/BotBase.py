from abc import ABCMeta, abstractmethod


class BotBase(metaclass=ABCMeta):
    @abstractmethod
    def send_text(self, chat_id, text):
        pass

    @abstractmethod
    def send_image(self, chat_id, image):
        pass

    @abstractmethod
    def send_voice_message(self, chat_id, voice_message):
        pass

    @abstractmethod
    def send_chat_action(self, chat_id, action):
        pass

    @abstractmethod
    def schedule_message(self, chat_id, text, delay):
        pass
