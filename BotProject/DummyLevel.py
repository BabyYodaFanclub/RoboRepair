from datetime import timedelta

from telegram import ChatAction

from BotBase import BotBase
from LevelBase import LevelBase
from State import State


class DummyLevel(LevelBase):

    def __init__(self):
        super().__init__()

    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        bot.send_chat_action(chat_id, ChatAction.TYPING)
        bot.schedule_message(chat_id, f'Hallo {global_state.name}!', timedelta(seconds=5))
        global_state.name = 'nameee'

        return self

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        pass
