import io
from datetime import timedelta

from telegram import ChatAction

from BotBase import BotBase
from LevelBase import LevelBase
from State import State


class SetupLevel(LevelBase):
    def __init__(self):
        self.current_dialog = io.open("./Levels/Setup/setup.dialog", mode="r", encoding="UTF-8").readlines()
        self.n = 0
        self.send_type = None

    def accept_chat_start(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        send_type = self.evaluate_send_type(self.current_dialog[self.n])
        if send_type == "none":
            bot.schedule_message(chat_id, self.current_dialog[self.n], timedelta(seconds=2))
        if send_type == "iterative":
            bot.send_iteratively_edited_message(chat_id, self.current_dialog[self.n].split())
        return self

    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        self.evaluate_next_line(text)
        return self

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        pass

    def next_line(self):
        self.evaluate_next_line(self.current_dialog[self.n])

    def evaluate_next_line(self, next_line: str):
        params = self.extract_line_params(self.current_dialog[0])
        if 'w' in params:
            valid_keywords = params['w']
            if valid_keywords == None:
                self.n += 1
            elif any(keyword in next_line for keyword in valid_keywords):
                pass
        if 't' in params:
            self.send_type = "iterative"
        if 'd' in params:
            self.send_type = "delayed"

    def trim_line(self, next_line: str):
        return next_line.split("] ")[2]