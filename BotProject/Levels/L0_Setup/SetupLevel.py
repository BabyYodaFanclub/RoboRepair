import io
import os

from BotBase import BotBase
from LevelBase import LevelBase
from Speech import Speech
from State import State

from DialogActions import DialogActionFactory


class SetupLevel(LevelBase):

    @staticmethod
    def current_dir():
        return os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        current_dialog = io.open(
            self.current_dir()
            # + os.path.basename(__file__).lower()
            + '/setup' + ".dialog", mode="r", encoding="UTF-8"
        ).readlines()

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

    @staticmethod
    def is_send_action(d):
        return isinstance(d, ImmediateNextAction) or isinstance(d, SendPictureAction)

    def accept_chat_start(self, bot: BotBase, chat_id: str, global_state: State) -> 'LevelBase':
        c_dialog = self.current_dialog()
        if self.is_send_action(c_dialog):
            c_dialog.do_action_text(bot, chat_id, '', global_state, lambda x: self.set_current_dialog(x))

        return self

    def set_current_dialog(self, dialog_position: int):
        self.dialog_position = dialog_position


    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        c_dialog = self.current_dialog()

        if isinstance(c_dialog, EndLevelAction):
            # todo next-level
            return self

        c_dialog.do_action_text(bot, chat_id, text, global_state,
                                lambda dialog_pos: self.walk_dialog(dialog_pos, bot, chat_id, text, global_state))

        return self

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        c_dialog = self.current_dialog()
        if isinstance(c_dialog, EndLevelAction):
            # todo next-level
            return self

        speech = Speech()
        text = speech.speech_to_text(voice_message)

        c_dialog.do_action_voice(bot, chat_id, text, global_state,
                                lambda dialog_pos: self.walk_dialog_voice(dialog_pos, bot, chat_id, text, global_state))

        return self

    def walk_dialog(self, dialog_position: int, bot: BotBase, chat_id: str, text: str, global_state: State):
        self.dialog_position = dialog_position

        c_dialog = self.current_dialog()

        if not self.is_send_action(c_dialog):
            return

        c_dialog.do_action_text(bot, chat_id, text, global_state,
                                lambda dialog_pos: self.walk_dialog(dialog_pos, bot, chat_id, text, global_state))

    def walk_dialog_voice(self, dialog_position: int, bot: BotBase, chat_id: str, text: str, global_state: State):
        self.dialog_position = dialog_position

        c_dialog = self.current_dialog()

        if not self.is_send_action(c_dialog):
            return

        c_dialog.do_action_voice(bot, chat_id, text, global_state,
                                lambda dialog_pos: self.walk_dialog(dialog_pos, bot, chat_id, text, global_state))
