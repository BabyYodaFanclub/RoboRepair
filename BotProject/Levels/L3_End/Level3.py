from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from DialogActions import ImmediateNextAction, DialogMode
from State import State


class Level3(AbstractLevel):

    def __init__(self):
        super().__init__()

        self.initialised = False
        self.package_has_arrived = False

    def get_file(self):
        return __file__

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        if not self.initialised:
            self.initialised = True
            print('queuing got there save message')
            delay = 4 * 24 * 60 * 60
            ImmediateNextAction.static_send(
                bot,
                global_state,
                'I got there safely, thanks again $user_name, you\'r the best human i ever met!',
                lambda *x: self.set_package_has_arrived(),
                DialogMode.REGULAR,
                delay
            )

            return

        if self.package_has_arrived:
            self.set_level_completed()
            ImmediateNextAction.static_send(
                bot,
                global_state,
                'If you want to help other Robos like me, type `/start`',
                lambda *x: self.end_level(bot, global_state)
            )
        else:
            ImmediateNextAction.static_send(
                bot,
                global_state,
                'Stand by I am delivering my package.',
                lambda *x: None
            )

    def set_package_has_arrived(self):
        self.package_has_arrived = True

    def end(self, global_state: State) -> 'LevelBase':
        rescued = global_state.achievements['rescued'] if global_state.achievements['rescued'] else 0
        global_state.achievements['rescued'] = rescued + 1
        global_state.finished.append(global_state.values)
        global_state.values = {}
        return 'SetupLevel'()


