from AbstractLevel import AbstractLevel
from BotBase import BotBase
from ChatType import ChatType
from MessageSequence import MessageSequence
from State import State
from DialogActions import ImmediateNextAction, SendPictureAction


class Level1(AbstractLevel):

    def __init__(self):
        self.camera_is_on = False

        self.set_message_sequence('00_start', self.end_dialog_1)

        self.valid_keys = {
            "how can i help": lambda *x: self.set_message_sequence("help"),
            "what is your model?": lambda *x: self.set_message_sequence("model"),
            "which model are you?": lambda *x: self.set_message_sequence("model"),
            "what is your model": lambda *x: self.set_message_sequence("model"),
            "which model are you": lambda *x: self.set_message_sequence("model"),
            "show me what you see": self.send_visuals,
            "what do you see?": self.send_visuals,
            "what do you see": self.send_visuals,
            "hokus pokus camerus restartikus": lambda *x: self.set_message_sequence("camrestart", self.end_camera_restart_dialog())
        }

    def send_visuals(self, bot: BotBase, global_state: State):
        if not self.camera_is_on:
            ImmediateNextAction("I can see this:", 0, []).send(bot, global_state, lambda *x:
            SendPictureAction('', 0, [self.current_dir() + "/01black.png"]).send(bot, global_state, lambda *x: None)
                                                               )
        else:
            ImmediateNextAction("I can see this:", 0, []).send(bot, global_state, lambda *x:
            SendPictureAction('', 0, [self.current_dir() + "everything good.png"]).send(bot, global_state, lambda *x: None)
                                                               )

    def get_file(self):
        return __file__

    def level_resume(self, bot: BotBase, global_state: State, chat_type: ChatType, message) -> 'LevelBase':
        if chat_type is ChatType.VOICE:
            ImmediateNextAction("", 0, []).send_error(bot, global_state, lambda *x: None)
            return

        message = message.lower()
        for key, val in self.valid_keys.items():
            if message in key:
                val(bot, global_state)
        ImmediateNextAction("", 0, []).send_error(bot, global_state, lambda *x: None)


    def end(self, global_state: State) -> 'LevelBase':
        pass

    def check_for_win(self) -> bool:
        return self.camera_is_on

    def end_dialog_1(self):
        self.message_sequence = None

    def end_camera_restart_dialog(self):
        self.camera_is_on = True
        self.message_sequence = None