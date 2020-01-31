from telegram import Update, ChatAction, Message, Bot
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


class BotRepair:
    def __init__(self):
        self.bot_token = open('./bot_token', 'r').read()
        self.start_bot()
        print('Bot started')

    def start_bot(self):
        updater = Updater(self.bot_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.text, self.message_callback))
        dispatcher.add_handler(MessageHandler(Filters.voice, self.voice_callback))

        updater.start_polling()

        # j = updater.job_queue
        # j.run_repeating(self.send_subs, interval=3600, first=600)

    def message_callback(self, update: Update, context: CallbackContext):
        context.chat_data['current_message'] = update.message.text

        print(f'update: {update}')
        print(f'chat_data: {context.chat_data}')
        print(f'user_data: {context.user_data}')

        if not context.chat_data['initialized']:
            context.chat_data['initialized'] = True
            pass
        else:
            context.chat_data['current_level'] = \
                context.chat_data['current_level'].accept_text_message(self, update.effective_chat.id)

    def voice_callback(self, update: Update, context: CallbackContext):
        pass

    def send_text(self, chat_id, text) -> Message:
        return Bot(self.bot_token).send_message(chat_id, text)

    def send_image(self, chat_id, image) -> Message:
        return Bot(self.bot_token).send_photo(chat_id, image)

    def send_voice_message(self, chat_id, voice_message) -> Message:
        return Bot(self.bot_token).send_voice(chat_id, voice_message)

    def send_chat_action(self, chat_id, action: ChatAction) -> Message:
        return Bot(self.bot_token).send_chat_action(chat_id, action)


if __name__ == "__main__":
    bot = BotRepair()
