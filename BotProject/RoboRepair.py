from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


class BotRepair:
    def __init__(self, config_file):
        self.conf_file = config_file

        self.start_bot("BOT TOKEN")
        print('Bot started')

    def start_bot(self, bot_token):
        updater = Updater(token=bot_token)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.all, self.callback))

        updater.start_polling()

        # j = updater.job_queue
        # j.run_repeating(self.send_subs, interval=3600, first=600)

    def callback(self, update: Update, context: CallbackContext):
        pass
