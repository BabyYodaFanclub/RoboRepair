import io

from telegram import ChatAction

from BotBase import BotBase
from LevelBase import LevelBase
from State import State


class SetupLevel(LevelBase):
    def __init__(self):
        self.currentDialog = io.open("./Levels/Setup/setup.dialog", mode="r", encoding="UTF-8").readlines()
        self.n = 0


    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        send_type = self.evaluate_next_line(self.currentDialog[self.n])
        return self

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        pass

    def evaluate_next_line(self, next_line: str):
        line = next_line.split()
        if line[0] == "[i]":
            return "i"
