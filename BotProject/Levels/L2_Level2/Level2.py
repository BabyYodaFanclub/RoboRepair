from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from DialogActions import ImmediateNextAction
from State import State
from Levels.L3_End.Level3 import Level3


class Level2(AbstractLevel):

    def __init__(self):
        self.has_leg = False
        self.is_at_ship = False
        self.is_in_spaceship = False
        self.has_blowtorch = False
        self.is_repaired = False

        self.set_message_sequence("00_start")

        self.valid_keys = {
            "take leg": lambda b, s: self.run_message_sequence(b, s, "01_take_leg", self.end_take_leg),
            "go to ship": lambda b, s: self.run_message_sequence(b, s, "02_go_ship", self.end_go_ship),
            "go to spaceship": lambda b, s: self.run_message_sequence(b, s, "02_go_ship", self.end_go_ship),
            "go to ufo": lambda b, s: self.run_message_sequence(b, s, "02_go_ship", self.end_go_ship)
        }

    def get_file(self):
        return __file__

    def run_message_sequence(self, bot, global_state, name: str, callback: callable = None):
        self.set_message_sequence(name, callback)
        self.start_message_sequence(bot, global_state)

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        if chat_type is ChatType.VOICE:
            ImmediateNextAction.static_send_error(bot, global_state)
            return

        message = message.lower()

        for key, val in self.valid_keys.items():
            if message == key or key in message:
                val(bot, global_state)
                return

        ImmediateNextAction.static_send_error(bot, global_state)

    def end(self, global_state: State) -> 'LevelBase':
        return Level3()

    def check_for_win(self, global_state: State):
        pass

    def end_current_dialog(self):
        self.message_sequence = None

    def end_take_leg(self):
        self.end_current_dialog()
        self.has_leg = True
        del self.valid_keys["take leg"]

    def end_go_ship(self):
        self.end_current_dialog()
        self.is_at_ship = True
        del self.valid_keys["go to ship"]
        del self.valid_keys["go to spaceship"]
        del self.valid_keys["go to ufo"]

