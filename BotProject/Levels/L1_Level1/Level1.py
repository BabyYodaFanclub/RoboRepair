from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from Levels.L2_Level2.Level2 import Level2
from State import State
from DialogActions import ImmediateNextAction, SendPictureAction


class Level1(AbstractLevel):

    def __init__(self):
        super().__init__()

        self.camera_is_on = False

        self.set_message_sequence('00_start')

        self.valid_keys = {
            'help': (
                True,
                ['how can i help'],
                lambda b, s: self.run_message_sequence(b, s, "01_help")
            ),
            'model': (
                True,
                ['what is your model', 'which model are you'],
                lambda b, s: self.run_message_sequence(b, s, "01_model")
            ),
            'visuals': (
                True,
                ['show me what you see', 'what do you see'],
                self.send_visuals
            ),
            'cam_restart': (
                True,
                ['hokus pokus camerus restartikus'],
                lambda b, s: self.run_message_sequence(b, s, "02_cam_restart", self.end_camera_restart_dialog)
            )
        }

    def send_visuals(self, bot: BotBase, global_state: State):
        if not self.camera_is_on:
            ImmediateNextAction.static_send(
                bot,
                global_state,
                "I can see this:",
                lambda *x: SendPictureAction.static_send(
                    bot,
                    global_state,
                    self.current_dir() + "/01black.png",
                    lambda *y: None)
            )
        else:
            ImmediateNextAction.static_send(
                bot,
                global_state,
                "I can see this:",
                lambda *x: SendPictureAction.static_send(
                    bot,
                    global_state,
                    self.current_dir() + "everything good.png",
                    lambda *y: None)
            )

    def get_file(self):
        return __file__

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message):
        if chat_type is ChatType.VOICE:
            ImmediateNextAction.static_send_error(bot, global_state)
            return

        super().level_resume(bot, global_state, chat_type, message)

    def end(self, global_state: State) -> 'LevelBase':
        return Level2()

    def end_camera_restart_dialog(self, bot: BotBase, global_state: State):
        self.camera_is_on = True
        self.message_sequence = None

        self.end_level(bot, global_state)
