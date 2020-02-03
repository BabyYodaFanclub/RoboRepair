from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from DialogActions import ImmediateNextAction
from State import State
from Levels.L3_End.Level3 import Level3


class Level2(AbstractLevel):

    def __init__(self):
        super().__init__()

        self.has_leg = False
        self.is_at_ship = False
        self.is_in_spaceship = False
        self.has_blowtorch = False
        self.is_repaired = False

        self.set_message_sequence("00_start")

        self.valid_keys = {
            'take_leg': (
                True,
                ['take leg', 'take the leg'],
                lambda b, s: self.run_message_sequence(b, s, "01_take_leg", self.end_take_leg)
            ),
            'go_ship': (
                False,
                ['go to ship', 'go to the ship', 'go to spaceship', 'go to the spaceship', 'go to ufo', 'go to the ufo'],
                lambda b, s: self.run_message_sequence(b, s, "02_go_ship", self.end_go_ship)
            )
        }

    def get_file(self):
        return __file__

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        if chat_type is ChatType.VOICE:
            ImmediateNextAction.static_send_error(bot, global_state)
            return

        super().level_resume(bot, global_state, chat_type, message)

    def end(self, global_state: State) -> 'LevelBase':
        return Level3()

    def end_current_dialog(self):
        self.message_sequence = None

    def toggle_enable_valid_key(self, key: str, enable: bool = True):
        active, variants, callback = self.valid_keys[key]
        if active == enable:
            return

        self.valid_keys[key] = (enable, variants, callback)

    def end_take_leg(self, bot: BotBase, global_state: State):
        self.end_current_dialog()
        self.has_leg = True
        self.toggle_enable_valid_key('take_leg', False)
        self.toggle_enable_valid_key('go_ship', True)

    def end_go_ship(self, bot: BotBase, global_state: State):
        self.end_current_dialog()
        self.is_at_ship = True
        self.toggle_enable_valid_key('go_ship', False)

        self.end_level(bot, global_state)

