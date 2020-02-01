from datetime import timedelta

from telegram import ChatAction

from BotBase import BotBase
from LevelBase import LevelBase
from State import State

from Speech import Speech


class SpeechLevel(LevelBase):

    def __init__(self):
        super().__init__()

    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        global_state.name = text

        speech = Speech()

        file = speech.textToSpeech(f'Hallo {global_state.name}!')

        bot.send_voice_message(chat_id, file)

        return self

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':

        speech = Speech()

        text = speech.speechToText(voice_message)

        bot.send_text(chat_id, text)

        return self
