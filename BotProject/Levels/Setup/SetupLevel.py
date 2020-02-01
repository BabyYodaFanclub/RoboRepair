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

    def accept_chat_start(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        send_type = self.evaluate_send_type(self.current_dialog[self.n])
        if send_type == "none":
            bot.schedule_message(chat_id, self.current_dialog[self.n], timedelta(seconds=2))
        if send_type == "iterative":
            bot.send_iteratively_edited_message(chat_id, self.current_dialog[self.n].split())
        return self

    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        send_type = self.evaluate_send_type(self.current_dialog[self.n])
        print(send_type)
        if send_type == "none":
            bot.schedule_message(chat_id, self.current_dialog[self.n], timedelta(seconds=2))
        if send_type == "iterative":
            bot.send_iteratively_edited_message(chat_id, self.trim_line(self.current_dialog[self.n]).split())
        if send_type == "delayed":
            bot.delayed_type_message(chat_id, self.trim_line(self.current_dialog[self.n]))
        return self

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        pass

    def evaluate_next_line(self, next_line: str):
        line = next_line.split()
        if line[0] == "[i]":
            return "i"

    def evaluate_send_type(self, next_line: str):
        line = next_line.split()
        print(line[1])
        if line[1] == "[]":
            return "none"
        if line[1] == "[it]":
            return "iterative"
        if line[1] == "[de]":
            return "delayed"

    def trim_line(self, next_line: str):
        return next_line.split("] ")[2]