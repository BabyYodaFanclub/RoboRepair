from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from LevelBase import LevelBase
from Levels.L1_Level1.Level1 import Level1
from MessageSequence import MessageSequence
from State import State


class SetupLevel(AbstractLevel):

    def get_file(self):
        return __file__

    def start(self, bot: BotBase, global_state: State) -> 'LevelBase':
        self.message_sequence = MessageSequence(self.current_dir(), 'setup', self.end_message_sequence())
        self.message_sequence.start(bot, global_state)
        return self

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message) -> 'LevelBase':
        self.end()

    def end(self, global_state: State) -> 'LevelBase':
        return Level1()

    def check_for_win(self, global_state: State):
        pass
