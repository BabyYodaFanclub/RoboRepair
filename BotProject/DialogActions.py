
from abc import ABCMeta, abstractmethod
from datetime import timedelta
from enum import Enum, unique
from random import randint
import io

from telegram import ChatAction

from BotBase import BotBase
from ChatType import ChatType
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

    yes = list(map(lambda c: c.strip().lower(), io.open('./Levels/YES.dialog', mode="r", encoding="UTF-8").readlines()))
    no = list(map(lambda c: c.strip().lower(), io.open('./Levels/NO.dialog', mode="r", encoding="UTF-8").readlines()))

    def __init__(self, path):
        self.path = path + '/'
        self.index = 0

    def create(self, _type: str, params, text: str):
        text = text.strip()
        self.index = self.index + 1
        if _type == 'i':
            return ImmediateNextAction(text, self.index, params)
        if _type == 'w':
            params = list(map(lambda p: p.strip().lower(), params))
            return WaitForTextAction(text, self.index, params)
        if _type == 'a':
            params = list(map(lambda p: p.strip().lower(), params))
            return WaitForAudioAction(text, self.index, params)
        if _type == 'c':
            params = [self.yes, self.no, *params]
            return ChoiceAction(text, self.index, params)
        if _type == 's':
            return SaveVarAction(text, self.index, params)
        if _type == 'p':
            params[0] = self.path + params[0]
            return SendPictureAction(text, self.index, params)
        if _type == 'e':
            return EndLevelAction()


class DialogAction(metaclass=ABCMeta):
    index: 0
    text: ''
    params: {}

    def __init__(self, text: str, index: int, params):
        self.index = index
        self.params = params
        self.text = text

    def do(self, bot: BotBase, global_state: State, message, chat_type: ChatType, callback):
        if isinstance(self, DialogOutputAction):
            self.send(bot, global_state, callback)
        elif isinstance(self, DialogInputAction):
            self.receive(bot, global_state, message, chat_type, callback)

    def next_index(self):
        return self.index + 1

    def send_error(self, bot: BotBase, global_state: State, callback, text: str = ''):
        bot.send_chat_action(global_state.chat_id, ChatAction.TYPING)
        bot.schedule_message(global_state.chat_id,
                             DialogAction.get_unknown_command_text() if text == '' else text,
                             1, lambda *x: callback(self.index + 1))

    @staticmethod
    def static_send_error(bot: BotBase, global_state: State, text: str = ''):
        bot.send_chat_action(global_state.chat_id, ChatAction.TYPING)
        bot.schedule_message(global_state.chat_id,
                             DialogAction.get_unknown_command_text() if text == '' else text,
                             1, lambda *x: None)

    __unknown_commands = list(map(lambda c: c.strip(), io.open('./Levels/UNKNOWNCOMMAND.dialog',
                                                               mode="r",
                                                               encoding="UTF-8").readlines()))

    @staticmethod
    def get_unknown_command_text():
        return DialogAction.__unknown_commands[randint(0, len(DialogAction.__unknown_commands) -1)]


class EndLevelAction(DialogAction):

    def __init__(self):
        return


class DialogInputAction(DialogAction, metaclass=ABCMeta):

    @abstractmethod
    def receive(self, bot: BotBase, global_state: State, text: str, chat_type: ChatType, callback):
        pass


class DialogOutputAction(DialogAction, metaclass=ABCMeta):

    def send(self, bot: BotBase, global_state: State, callback):
        self.send_error(bot, global_state, callback)


class DialogWaitForTypeAction(DialogInputAction, metaclass=ABCMeta):

    @abstractmethod
    def type(self) -> ChatType:
        pass

    def receive(self, bot: BotBase, global_state: State, text: str, chat_type: ChatType, callback):
        if chat_type is not self.type():
            self.send_error(bot, global_state, lambda *x: callback(self.index), self.text)
            return

        correct = 0
        text = text.lower()
        for param in self.params:
            if param.lower().strip() in text:
                correct = correct + 1

        if correct >= 1 or len(self.params) == 0:
            callback(self.next_index())
            return

        self.send_error(bot, global_state, lambda *x: callback(self.index), self.text)


##################################
#         Output-Actions         #
##################################


class ImmediateNextAction(DialogOutputAction):

    def __init__(self, text: str, index: int, params):

        if len(params) > 0:
            self.mode = DialogMode(params[0])
        else:
            self.mode = DialogMode.REGULAR

        if len(params) > 1:
            self.delay = int(params[1])
        else:
            self.delay = 1

        self.text = text
        self.index = index

    def send(self, bot: BotBase, global_state: State, callback):
        self.static_send(bot, global_state, self.text, lambda *x: callback(self.next_index()),
                         self.mode, self.delay)

    @staticmethod
    def get_text(_text: str, global_state: State):
        t = _text
        for key, value in global_state.values.items():
            _text = _text.replace('$' + key, value)

        # if "$" in _text:
        #     raise Exception('Found $ in ' + t)

        return _text

    @staticmethod
    def static_send(bot: BotBase, global_state: State, text: str, callback: callable,
                    mode: DialogMode = DialogMode.REGULAR, delay: int = 1):

        chat_id = global_state.chat_id
        _text = ImmediateNextAction.get_text(text.strip(), global_state)

        if mode == DialogMode.REGULAR:
            bot.send_chat_action(chat_id, ChatAction.TYPING)
            bot.schedule_message(chat_id, _text, delay, lambda *x: callback())

        elif mode == DialogMode.DELAYED:
            bot.delayed_type_message(chat_id, _text, lambda *x: callback())

        elif mode == DialogMode.ITERATIVE:
            bot.send_iteratively_edited_message(chat_id, _text.split())
            callback()

        elif mode == DialogMode.VOICE:
            speech = Speech()
            bot.send_chat_action(chat_id, ChatAction.RECORD_AUDIO)
            audio_message = speech.text_to_speech(_text)
            bot.send_voice_message(chat_id, audio_message)
            callback()


class SendPictureAction(DialogOutputAction):

    def send(self, bot: BotBase, global_state: State, callback):
        self.static_send(bot, global_state, self.params[0], lambda *x: callback(self.next_index()))

    @staticmethod
    def static_send(bot: BotBase, global_state: State, image_path: str, callback: callable):
        bot.send_chat_action(global_state.chat_id, ChatAction.UPLOAD_PHOTO)
        bot.send_image(global_state.chat_id, open(image_path, 'rb'))
        callback()


##################################
#         WaitFor-Actions        #
##################################


class WaitForTextAction(DialogWaitForTypeAction):

    def type(self) -> ChatType:
        return ChatType.TEXT


class WaitForAudioAction(DialogWaitForTypeAction):

    def type(self) -> ChatType:
        return ChatType.VOICE

##################################
#          Input-Actions         #
##################################


class ChoiceAction(DialogInputAction):

    def receive(self, bot: BotBase, global_state: State, text: str, chat_type: ChatType, callback):
        if chat_type is ChatType.VOICE:
            self.send_error(bot, global_state, lambda *x: callback(self.index - 1), self.text)
            return

        try:
            result = self.evaluate_choice(text.lower())
            callback(self.calc_line_number(self.params[2 if result else 3]))
        except Exception as e:
            callback(self.index - 1)

    def evaluate_choice(self, text: str):
        for y in self.params[0]:
            if y in text:
                return True

        for n in self.params[1]:
            if n in text:
                return False

        raise Exception('No answer is given')

    def calc_line_number(self, number: str):
        relative = '~' in number
        num = int(number.replace('~', ''))

        if relative:
            return self.index + num
        else:
            return num


class SaveVarAction(DialogInputAction):

    def receive(self, bot: BotBase, global_state: State, text: str, chat_type: ChatType, callback):
        if chat_type is ChatType.VOICE:
            self.send_error(bot, global_state, lambda *x: callback(self.index - 1), self.text)
            return

        global_state.values[self.params[0]] = text
        callback(self.next_index())
