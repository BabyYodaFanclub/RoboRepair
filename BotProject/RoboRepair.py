import os
from datetime import timedelta, datetime

from telegram import Update, ChatAction, Message, Bot
from telegram.ext import CallbackContext, CommandHandler, Job
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from BotBase import BotBase
from DummyLevel import DummyLevel
from LevelBase import LevelBase
from State import State


class BotRepair(BotBase):
    def __init__(self):
        if not os.path.exists('.tmp'):
            os.makedirs('.tmp')

        self.bot_token = open('./bot_token', 'r').read()
        self.updater = Updater(self.bot_token, use_context=True)
        self.iterating_chats = {}

    def start_bot(self):
        dispatcher = self.updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', self.__start_callback))
        dispatcher.add_handler(CommandHandler('reset', self.__reset_callback))
        dispatcher.add_handler(MessageHandler(Filters.text, self.__message_callback))
        dispatcher.add_handler(MessageHandler(Filters.voice, self.__voice_callback))
        dispatcher.add_error_handler(self.__on_error)

        j = self.updater.job_queue
        j.run_repeating(self.__send_cries_for_help, interval=3600, first=3600)

        self.updater.start_polling()

    def __send_cries_for_help(self, job: Job):
        for chat_id, chat_data in self.updater.dispatcher.chat_data.items():
            last = chat_data['last_message_timestamp']
            seconds_ago = (datetime.now() - last).total_seconds()
            if seconds_ago > 24 * 60 * 60:
                chat_data['last_message_timestamp'] = datetime.now()
                chat_data['current_level'] = \
                    chat_data['current_level'].accept_chat_start(self,
                                                                 chat_id,
                                                                 chat_data['state'])

    def __reset_callback(self, update: Update, context: CallbackContext):
        self.iterating_chats[update.effective_chat.id] = None
        context.chat_data.clear()
        context.chat_data.update(self.__create_new_chat_session())

    @staticmethod
    def __on_error(update: Update, context: CallbackContext):
        print(f'Error: {context.error}')

    def __ensure_session(self, context: CallbackContext):
        if 'initialized' not in context.chat_data:
            context.chat_data.update(self.__create_new_chat_session())

    @staticmethod
    def __create_new_chat_session():
        return {'initialized': True, 'state': State(), 'current_level': DummyLevel()}

    def __start_callback(self, update: Update, context: CallbackContext):
        self.__ensure_session(context)
        context.chat_data['current_level'] = \
            context.chat_data['current_level'].accept_chat_start(self,
                                                                 update.effective_chat.id,
                                                                 context.chat_data['state'])

    def __message_callback(self, update: Update, context: CallbackContext):
        context.chat_data['last_message_timestamp'] = datetime.now()
        self.__ensure_session(context)
        self.iterating_chats[update.effective_chat.id] = None

        print(f'update: {update}')
        print(f'chat_data: {context.chat_data}')

        context.chat_data['current_level'] = \
            context.chat_data['current_level'].accept_text_message(self,
                                                                   update.effective_chat.id,
                                                                   update.effective_message.text,
                                                                   context.chat_data['state'])

    def __voice_callback(self, update: Update, context: CallbackContext):
        context.chat_data['last_message_timestamp'] = datetime.now()
        self.__ensure_session(context)
        self.iterating_chats[update.effective_chat.id] = None

        print(f'update: {update}')
        print(f'chat_data: {context.chat_data}')
        print(f'user_data: {context.user_data}')

        context.chat_data['current_level'] = \
            context.chat_data['current_level'].accept_voice_message(self,
                                                                    update.effective_chat.id,
                                                                    update.effective_message.voice,
                                                                    context.chat_data['state'])

    def update_current_level(self, chat_id: str, level: LevelBase):
        self.updater.dispatcher.chat_data[chat_id]['current_level'] = level

    def send_text(self, chat_id: str, text: str) -> Message:
        return Bot(self.bot_token).send_message(chat_id, text)

    def send_image(self, chat_id: str, image) -> Message:
        return Bot(self.bot_token).send_photo(chat_id, image)

    def send_voice_message(self, chat_id: str, voice_message) -> Message:
        return Bot(self.bot_token).send_voice(chat_id, voice_message)

    def send_chat_action(self, chat_id: str, action: ChatAction) -> Message:
        return Bot(self.bot_token).send_chat_action(chat_id, action)

    def schedule_message(self, chat_id, text: str, delay: timedelta, callback):
        return self.updater.dispatcher.job_queue.run_once(
            lambda x: self.schedule_message(chat_id, text, delay, callback),
            delay)

    def send_scheduled_message(self, chat_id, text, callback):
        self.send_text(chat_id, text)
        callback()

    def send_iteratively_edited_message(self, chat_id: str, texts: list):
        time_per_message = timedelta(milliseconds=250)
        message = self.send_text(chat_id, texts[0])
        self.iterating_chats[chat_id] = message.message_id
        self.updater.dispatcher.job_queue.run_once(lambda x: self.__iteratively_edit_message(message, texts,
                                                                                             1,
                                                                                             time_per_message),
                                                   time_per_message)

    def __iteratively_edit_message(self, message: Message, texts: list, current_item: int, time_per_message: timedelta):
        if self.iterating_chats[message.chat_id] != message.message_id or current_item > 50:
            return

        message = message.edit_text(texts[current_item % len(texts)])
        current_item += 1

        self.updater.dispatcher.job_queue.run_once(lambda job: self.__iteratively_edit_message(message,
                                                                                               texts,
                                                                                               current_item,
                                                                                               time_per_message),
                                                   time_per_message)

    def delayed_type_message(self, chat_id: str, text: str, callback):
        time_per_char = timedelta(milliseconds=100)
        text = text.strip()
        message = self.send_text(chat_id, text[0])
        self.updater.dispatcher.job_queue.run_once(lambda x: self.__delayed_type_message_part(message,
                                                                                              text,
                                                                                              2,
                                                                                              time_per_char,
                                                                                              callback),
                                                   time_per_char)

    def __delayed_type_message_part(self, message: Message, text: str, current_char: int, time_per_char: timedelta,
                                    callback):
        while text[0:current_char].strip() == message.text:
            current_char += 1
        partial_text = text[0:current_char]
        message = message.edit_text(partial_text)

        if current_char == len(text):
            callback()
            return

        self.updater.dispatcher.job_queue.run_once(lambda job: self.__delayed_type_message_part(message,
                                                                                                text,
                                                                                                current_char + 1,
                                                                                                time_per_char,
                                                                                                callback),
                                                   time_per_char)


if __name__ == "__main__":
    bot = BotRepair()
    bot.start_bot()
    print('Bot started')
