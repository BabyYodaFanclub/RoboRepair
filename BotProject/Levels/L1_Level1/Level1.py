from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from MessageSequence import MessageSequence
from State import State
from DialogActions import ImmediateNextAction


class Level1(AbstractLevel):

    def __init__(self):
        self.has_entered_serial = False
        self.brightness = 2400
        self.focus = False
        self.distortion_x = 1
        self.distortion_y = 1
        self.coordinate_system = False

        self.message_sequence = MessageSequence(self.current_dir(), "00_start", lambda x: self.end_dialog_1())

        self.valid_keys = {
            "how can I help": lambda: self.set_message_sequence("help"),
            "what is your model?": lambda: self.set_message_sequence("model"),
            "which model are you?": lambda: self.set_message_sequence("model"),
            "what is your model": lambda: self.set_message_sequence("model"),
            "which model are you": lambda: self.set_message_sequence("model"),
            "show me what you see": lambda: self.set_message_sequence("visuals"),
            "what do you see?": lambda: self.set_message_sequence("visuals"),
            "what do you see": lambda: self.set_message_sequence("visuals"),
            "hokus pokus camerus restartikus": lambda : self.set_message_sequence("camrestart")
        }

    def set_message_sequence(self, name: str):
        self.message_sequence = MessageSequence(self.current_dir(), "help", self.end_message_sequence)

    def get_file(self):
        return __file__

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message) -> 'LevelBase':
        if chat_type is ChatType.VOICE:
            ImmediateNextAction("", 0, []).send_error(bot, global_state, lambda: None)
            return

        message = message.lower()
        for key, val in self.valid_keys.items():
            if message in key:
                val()
        return self


    def end(self, global_state: State) -> 'LevelBase':
        pass



    def check_for_win(self) -> bool:
        return self.has_entered_serial and self.brightness == 100 and self.focus \
            and self.distortion_x == 0 and self.distortion_y == 0

    def end_dialog_1(self):
        self.message_sequence = None
