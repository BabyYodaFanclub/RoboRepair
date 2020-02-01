from telegram import ChatAction

from BotBase import BotBase
from LevelBase import LevelBase
from State import State


class DummyLevel(LevelBase):

    def __init__(self):
        super().__init__()

    def accept_chat_start(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        bot.send_text(chat_id, 'TEST')
        return self

    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        bot.send_chat_action(chat_id, ChatAction.TYPING)
        # bot.delayed_type_message(chat_id, f'Hallo!\n{text}')
        # bot.send_iteratively_edited_message(chat_id, ['Hallo', 'Hola', 'Hiho','Hallo', 'Hola', 'Hiho','Hallo', 'Hola', 'Hiho','Hallo', 'Hola', 'Hiho'])

        return self

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        return self
