from decouple import config
import telebot
import NLP.dialog as dialog
import NLP.execution as execution
from AbstractMessagingManager import AbstractMessagingManager
    
class TelegramManager(AbstractMessagingManager):

    api_key = config('TELEGRAM_TOKEN')        

    bot = telebot.TeleBot(api_key)

    #@bot.message_handler(commands=['start', 'help'])
    #def send_welcome(self, message):
    #    self.bot.reply_to(message, "howdy")

    @bot.message_handler(func=lambda message: True)
    def send_message(self, message):
        msg = message
        print(msg.text)
        intent = dialog.askGoogle(msg.text)
        reply =  execution.findAnswer(intent)
        self.bot.reply_to(msg, reply)

    def send_file(self):
        return 0

    def receive_file(self):
        return 0

    def receive_message(self):
        return 0

    def start_polling(self):
        self.bot.polling(self)
