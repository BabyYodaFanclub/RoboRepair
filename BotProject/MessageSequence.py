import io
import os

from BotBase import BotBase
from ChatType import ChatType
from State import State
from DialogActions import DialogActionFactory, DialogOutputAction, EndLevelAction


class MessageSequence:

    def __init__(self, path, name, end_callback: callable):
        current_dialog = io.open(
            path
            + '/' + name + ".dialog", mode="r", encoding="UTF-8"
        ).readlines()

        self.end_callback = end_callback

        self.dialog_position = 1

        self.actions = []

        dialog_factory = DialogActionFactory(path)
        for line in current_dialog:

            tmp = line.split(']')
            tmp = list(map(lambda b: b.replace('[', ''), tmp))

            t, settings = tmp[0].split('=') if '=' in tmp[0] else [tmp[0], '']

            params = settings.split(',') if len(settings) > 0 else []

            text = tmp[1] if len(tmp) > 1 else ''

            self.actions.append(dialog_factory.create(t, params, text))

    def current_dialog(self):
        while callable(self.dialog_position):
            self.dialog_position = self.dialog_position()

        if self.dialog_position >= len(self.actions) or self.dialog_position < 0:
            return EndLevelAction()

        return self.actions[self.dialog_position - 1]

    def start(self, bot: BotBase, global_state: State):
        current = self.current_dialog()
        if isinstance(current, EndLevelAction):
            self.end()
            return

        if isinstance(current, DialogOutputAction):
            current.send(bot, global_state,
                         lambda pos: self.walk_dialog(bot, global_state, pos))

    def resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        current = self.current_dialog()

        if isinstance(current, EndLevelAction):
            self.end()
            return

        current.do(bot, global_state, message, chat_type,
                   lambda pos: self.walk_dialog(bot, global_state, pos))

    def end(self):
        callback = self.end_callback
        callback()

    def walk_dialog(self, bot: BotBase, global_state: State, dialog_position: int):
        self.dialog_position = dialog_position

        current = self.current_dialog()

        if isinstance(current, EndLevelAction):
            self.end()
            return

        if isinstance(current, DialogOutputAction):
            current.send(bot, global_state,
                         lambda pos: self.walk_dialog(bot, global_state, pos))
