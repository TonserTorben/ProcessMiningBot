from decouple import config
import telebot
import requests
import os

from IM.reply_enum import ReplyType
import IM.IMManager as manager
    

api_key = config('TELEGRAM_TOKEN')
bot = telebot.TeleBot(api_key)

#@bot.message_handler(commands=['start', 'help'])
#def send_welcome(self, message):
#    self.bot.reply_to(message, "howdy")

@bot.message_handler(func=lambda message: True)
def receive_message(message):
    msg = message.text 
    chat_id = message.chat.id
    reply, reply_type = manager.get_intention(msg)

    if (reply_type == ReplyType.text):
        send_message(chat_id, reply)
    elif (reply_type == ReplyType.photo):
        
        try:
            bot.send_chat_action(chat_id, "upload_photo")
            photo = open(reply, 'rb')
            send_photo(chat_id, photo)
        except Exception as e: 
            print(e)
    elif (reply_type == ReplyType.video):
        send_video(chat_id, reply)

@bot.message_handler(content_types=['document'])
def receive_file(message):
    file_info = bot.get_file(message.document.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(api_key, file_info.file_path))
    chat_id = message.chat.id
    send_message(chat_id, 'Thanks for the file')

def send_message(chat_id, message):
    #bot.reply_to(msg, reply)
    bot.send_message(chat_id, message, parse_mode="html")

def send_photo(chat_id, photo):
    bot.send_photo(chat_id, photo)

def send_video(chat_id, video):
    bot.send_video(chat_id, video)

def start_bot():
    bot.polling()
