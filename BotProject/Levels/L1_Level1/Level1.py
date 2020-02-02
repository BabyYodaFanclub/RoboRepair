from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from MessageSequence import MessageSequence
from State import State


class Level1(AbstractLevel):

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message) -> 'LevelBase':
        pass

    def end(self, global_state: State) -> 'LevelBase':
        pass

    def __init__(self):
        self.has_entered_serial = False
        self.brightness = 2400
        self.focus = False
        self.distortion_x = 1
        self.distortion_y = 1
        self.coordinate_system = False

        self.message_sequence = MessageSequence("00_start", lambda x: self.end_dialog_1())

    def check_for_win(self) -> bool:
        return self.has_entered_serial and self.brightness == 100 and self.focus \
            and self.distortion_x == 0 and self.distortion_y == 0

    def end_dialog_1(self):
        self.message_sequence = None
