import io
import os

from BotBase import BotBase
from ChatType import ChatType
from State import State
from DialogActions import DialogActionFactory, DialogOutputAction


class MessageSequence:

    @staticmethod
    def current_dir():
        return os.path.dirname(os.path.realpath(__file__))

    def __init__(self, name, end_callback: callable):
        current_dialog = io.open(
            self.current_dir()
            # + os.path.basename(__file__).lower()
            + '/' + name + ".dialog", mode="r", encoding="UTF-8"
        ).readlines()

        self.end_callback = end_callback

        self.dialog_position = 1

        self.actions = []

        i = 1
        for line in current_dialog:

            tmp = line.split(']')
            tmp = list(map(lambda b: b.replace('[', ''), tmp))

            if '=' in tmp[0]:
                t, settings = tmp[0].split('=')
            else:
                t, settings = [tmp[0], '']

            params = settings.split(',') if len(settings) > 0 else []

            if len(tmp) > 1:
                text = tmp[1]
            else:
                text = ''

            self.actions.append(DialogActionFactory.create(t, params, text, i))
            i = i + 1

    def current_dialog(self):
        return self.actions[self.dialog_position - 1]

    def start(self, bot: BotBase, global_state: State):
        current = self.current_dialog()
        if isinstance(current, DialogOutputAction):
            current.send(bot, global_state, lambda x: self.set_current_dialog(x))

    def resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        pass

    def end(self):
        self.end_callback()
