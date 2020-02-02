from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from LevelBase import LevelBase
from Levels.L1_Level1.Level1 import Level1
from State import State


class SetupLevel(AbstractLevel):

    def get_file(self):
        return __file__

    def start(self, bot: BotBase, global_state: State) -> 'LevelBase':
        self.set_message_sequence('setup', self.dialog_end)
        self.start_message_sequence(bot, global_state)
        return self

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        self.set_level_completed()

    def dialog_end(self):
        self.message_sequence = None
        self.set_level_completed()

    def end(self, global_state: State) -> 'LevelBase':
        return Level1()

    def check_for_win(self, global_state: State):
        pass
