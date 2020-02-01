import io
import os
from abc import ABCMeta
from enum import Enum, unique

from telegram import ChatAction

from BotBase import BotBase
from LevelBase import LevelBase
from Speech import Speech
from State import State


@unique
class DialogMode(Enum):
    UNDEFINED = '_'
    ITERATIVE = 't'
    DELAYED = 'd'
    REGULAR = 'r'
    VOICE = 'v'


class DialogActionFactory:

    @staticmethod
    def create(type: str, params, text: str, index):
        if type == 'i':
            return ImmediateNextAction(text, index, params)
        if type == 'w':
            return WaitForTextAction(text, index, params)
        if type == 'a':
            return WaitForAudioAction(text, index, params)
        if type == 'c':
            return ChoiceAction(text, index, params)
        if type == 's':
            return SaveVarAction(text, index, params)
        if type == 'e':
            return EndLevelAction(text, index, params)


class DialogAction(metaclass=ABCMeta):
    index: 0
    text: ''
    params: {}

    def __init__(self, text: str, index: int, params):
        self.index = index
        self.params = params
        self.text = text

    def do_action_text(self, bot: BotBase, chat_id: str, text: str, global_state: State, callback):
        bot.send_chat_action(chat_id, ChatAction.TYPING)
        bot.schedule_message(chat_id, DialogAction.get_unknown_command_text(), 1, lambda: callback(self.index))

    def do_action_voice(self, bot: BotBase, chat_id: str, text: str, global_state: State, callback):
        bot.send_chat_action(chat_id, ChatAction.TYPING)
        bot.schedule_message(chat_id, DialogAction.get_unknown_command_text(), 1, lambda: callback(self.index))
        return self.index

    def next_index(self):
        return self.index + 1

    def __str__(self):
        return self.index

    @staticmethod
    def get_unknown_command_text():
        # @todo read UNKNOWNCOMMMADN.dialog
        return 'Unknown Command'


class ImmediateNextAction(DialogAction):
    bot: None
    mode: DialogMode.UNDEFINED
    text: ''
    index: 0
    params: {}

    def __init__(self, text: str, index: int, params):

        if len(params) > 0:
            self.mode = DialogMode(params[0])
        else:
            self.mode = DialogMode.REGULAR

        self.params = {}

        if len(params) > 1:
            self.params['delay'] = params[1]
        else:
            self.params['delay'] = 1

        self.text = text
        self.index = index

    def do_action_text(self, bot: BotBase, chat_id: str, text: str, global_state: State, callback):
        self.send_message(bot, chat_id, global_state)
        callback(self.next_index())

    def do_action_voice(self, bot: BotBase, chat_id: str, text: str, global_state: State, callback):
        self.send_message(bot, chat_id, global_state)
        callback(self.next_index())

    def send_message(self, bot: BotBase, chat_id: str, global_state: State):
        if self.mode == DialogMode.REGULAR:
            bot.send_chat_action(chat_id, ChatAction.TYPING)
            bot.schedule_message(chat_id, self.get_text(global_state), 1, lambda: None)

        elif self.mode == DialogMode.DELAYED:
            tmp = self.get_text(global_state)
            print(tmp)
            bot.delayed_type_message(chat_id, tmp, lambda: None)

        elif self.mode == DialogMode.ITERATIVE:
            bot.send_iteratively_edited_message(chat_id, self.get_text(global_state).split())

        elif self.mode == DialogMode.VOICE:
            speech = Speech()
            bot.send_chat_action(chat_id, ChatAction.RECORD_AUDIO)
            audio_message = speech.text_to_speech(self.get_text(global_state))
            bot.send_voice_message(chat_id, audio_message)

    def get_text(self, global_state: State):
        _text = self.text

        for key, value in global_state.values.items():
            _text = _text.replace('$' + key, value)

        if "$" in _text:
            raise Exception('Found $ in ' + self.text)

        return _text


class WaitForTextAction(DialogAction):

    def do_action_text(self, bot: BotBase, chat_id: str, text: str, global_state: State, callback):
        correct = 0
        for param in self.params:
            if param in text:
                correct = correct + 1

        if correct > 1 or len(self.params) == 0:
            return self.next_index()

        _text = self.text if self.text else self.get_unknown_command_text()

        bot.send_chat_action(chat_id, ChatAction.TYPING)
        bot.schedule_message(chat_id, _text, 1, lambda: callback(self.index))


class WaitForAudioAction(DialogAction):

    def do_action_voice(self, bot: BotBase, chat_id: str, text: str, global_state: State, callback):
        correct = 0
        for param in self.params:
            if param in text:
                correct = correct + 1

        if correct > 1 or len(self.params) == 0:
            callback(self.next_index())
            return

        _text = self.text if self.text else self.get_unknown_command_text()

        bot.send_chat_action(chat_id, ChatAction.TYPING)
        bot.schedule_message(chat_id, _text, 1, lambda: callback(self.index))


class ChoiceAction(DialogAction):

    def do_action_text(self, bot: BotBase, chat_id: str, text: str, global_state: State, callback):
        try:
            result = self.evaluate_choice(text)
            callback(self.calc_line_number(self.params[0 if result else 1]))
        except Exception as e:
            callback(self.index - 1)

    def evaluate_choice(self, text: str):
        # @todo check valid answers!
        # raise Error if not in yes and not in no list
        return "yes" in text

    def calc_line_number(self, number: str):
        relative = '~' in number
        num = int(number.replace('~', ''))

        if relative:
            return self.index + num
        else:
            return num


class SaveVarAction(DialogAction):

    def do_action_text(self, bot: BotBase, chat_id: str, text: str, global_state: State, callback):
        global_state.values[self.params[0]] = text
        callback(self.next_index())


class EndLevelAction(DialogAction):
    pass


class SetupLevel(LevelBase):

    def __init__(self):
        current_dialog = io.open(
            os.path.dirname(os.path.realpath(__file__))
            # + os.path.basename(__file__).lower()
            + '/setup'
            + ".dialog", mode="r", encoding="UTF-8"
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

    def accept_chat_start(self, bot: BotBase, chat_id: str, global_state: State) -> 'LevelBase':

        if isinstance(self.current_dialog(), ImmediateNextAction):
            self.dialog_position = self.current_dialog().do_action_text(bot, chat_id, '', global_state, lambda: None)

        return self

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

        c_dialog.do_action_text(bot, chat_id, text, global_state,
                                lambda dialog_pos: self.walk_dialog(dialog_pos, bot, chat_id, text, global_state))

        return self

    def walk_dialog(self, dialog_position: int, bot: BotBase, chat_id: str, text: str, global_state: State):
        self.dialog_position = dialog_position

        c_dialog = self.current_dialog()
        print(self.dialog_position)

        if not isinstance(c_dialog, ImmediateNextAction):
            return

        c_dialog.do_action_text(bot, chat_id, text, global_state,
                                lambda dialog_pos: self.walk_dialog(dialog_pos, bot, chat_id, text, global_state))
