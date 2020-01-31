from telegram import Update, ChatAction, Message
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


class BotRepair:
    def __init__(self):
        self.start_bot(open('./bot_token', 'r').read())
        print('Bot started')

    def start_bot(self, bot_token):
        updater = Updater(bot_token, use_context=True)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.text, self.message_callback))
        dispatcher.add_handler(MessageHandler(Filters.voice, self.voice_callback))

        updater.start_polling()

        # j = updater.job_queue
        # j.run_repeating(self.send_subs, interval=3600, first=600)

    def message_callback(self, update: Update, context: CallbackContext):
        print(update)
        chat_data: dict = context.chat_data
        chat_data['current_message'] = update.message.text
        try:
            print(f'chat_data: {context.chat_data}')
            print(f'user_data: {context.user_data}')
        except BaseException as e:
            print(e)

    def voice_callback(self, update: Update, context: CallbackContext):
        pass

    def send_text(self, chat_id, text) -> Message:
        pass

    def send_image(self, chat_id, image) -> Message:
        pass

    def send_voice_message(self, chat_id, voice_message) -> Message:
        pass

    def send_chat_action(self, chat_id, action: ChatAction) -> Message:
        pass


if __name__ == "__main__":
    bot = BotRepair()
