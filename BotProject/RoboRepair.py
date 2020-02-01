from datetime import timedelta

from telegram import Update, ChatAction, Message, Bot
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from Bot import Bot
from DummyLevel import DummyLevel
from State import State


class BotRepair(Bot):
    def __init__(self):
        self.bot_token = open('./bot_token', 'r').read()
        self.updater = Updater(self.bot_token, use_context=True)

        self.start_bot()
        print('Bot started')

    def start_bot(self):
        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.text, self.message_callback))
        dispatcher.add_handler(MessageHandler(Filters.voice, self.voice_callback))
        dispatcher.add_error_handler(self.on_error)

        self.updater.start_polling()

        # j = updater.job_queue
        # j.run_repeating(self.send_subs, interval=3600, first=600)

    def on_error(self, update: Update, context: CallbackContext):
        print(f'Error: {context.error}')

    def ensure_session(self, context):
        if 'initialized' not in context.chat_data:
            context.chat_data.update(self.create_new_chat_session())

    @staticmethod
    def create_new_chat_session():
        return {'initialized': True, 'state': State(), 'current_level': DummyLevel()}

    def message_callback(self, update: Update, context: CallbackContext):
        try:
            context.chat_data['last_message'] = update.effective_message.text
            self.ensure_session(context)
            print(f'update: {update}')
            print(f'chat_data: {context.chat_data}')
            print(f'user_data: {context.user_data}')
        except Exception as e:
            print(e)
        context.chat_data['current_level'] = \
            context.chat_data['current_level'].accept_text_message(self,
                                                                   update.effective_chat.id,
                                                                   update.effective_message.text,
                                                                   context.chat_data['state'])

    def voice_callback(self, update: Update, context: CallbackContext):
        context.chat_data['last_message'] = 'Voice Message'
        self.ensure_session(context)

        print(f'update: {update}')
        print(f'chat_data: {context.chat_data}')
        print(f'user_data: {context.user_data}')

        context.chat_data['current_level'] = \
            context.chat_data['current_level'].accept_voice_message(self,
                                                                    update.effective_chat.id,
                                                                    update.effective_message.voice,
                                                                    context.chat_data['state'])

    def send_text(self, chat_id: str, text: str) -> Message:
        return Bot(self.bot_token).send_message(chat_id, text)

    def send_image(self, chat_id: str, image) -> Message:
        return Bot(self.bot_token).send_photo(chat_id, image)

    def send_voice_message(self, chat_id: str, voice_message) -> Message:
        return Bot(self.bot_token).send_voice(chat_id, voice_message)

    def send_chat_action(self, chat_id: str, action: ChatAction) -> Message:
        return Bot(self.bot_token).send_chat_action(chat_id, action)

    def schedule_message(self, chat_id, text: str, delay: timedelta):
        return self.updater.dispatcher.job_queue.run_once(lambda: self.send_text(chat_id, text), delay)


if __name__ == "__main__":
    bot = BotRepair()
