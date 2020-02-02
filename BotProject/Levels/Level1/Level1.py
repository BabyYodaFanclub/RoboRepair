from BotBase import BotBase
from LevelBase import LevelBase
from State import State


class Level1(LevelBase):

    def __init__(self):
        self.has_entered_serial = False
        self.brightness = 2400
        self.focus = False
        self.distortion_x = 1
        self.distortion_y = 1
        self.coordinate_system = False

    def accept_text_message(self, bot: BotBase, chat_id: str, text: str, global_state: State) -> 'LevelBase':
        pass

    def accept_voice_message(self, bot: BotBase, chat_id: str, voice_message, global_state: State) -> 'LevelBase':
        pass

    def check_for_win(self) -> bool:
        return self.has_entered_serial and self.brightness == 100 and self.focus \
            and self.distortion_x == 0 and self.distortion_y == 0

