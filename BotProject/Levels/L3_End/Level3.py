from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from DialogActions import ImmediateNextAction, DialogMode
from State import State


class Level3(AbstractLevel):

    def __init__(self):
        self.initialised = False
        pass

    def get_file(self):
        return __file__

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        if not self.initialised:
            delay = 4 * 24 * 60 * 60
            ImmediateNextAction.static_send(bot, global_state,
                                            'I got there safely, thanks again $user_name, you\'r the best human i ever met!',
                                            DialogMode.REGULAR, delay)
            self.initialised = True
            return

        ImmediateNextAction.static_send(bot, global_state, 'Stand by i am delivering my package.')

    def end(self, global_state: State) -> 'LevelBase':
        pass


