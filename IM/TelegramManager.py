from decouple import config
import telebot
import requests
import os, tempfile
from datetime import date

from Enums.reply_enum import ReplyType
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
    reply, reply_type = manager.handle_message(msg, chat_id, False)
    handle_message(chat_id, reply, reply_type)

@bot.message_handler(content_types=['document'])
def receive_file(message):
    file_info = bot.get_file(message.document.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(api_key, file_info.file_path))
    chat_id = message.chat.id
    #_, tmp_file = tempfile.mkstemp()
    #open(tmp_file, 'wb').write(file.content)
    user = message.from_user
    name = user.username if user.username != None else user.first_name + " " + user.last_name
    file_i = {"name": message.document.file_name,
              "file": file, 
              "user": name,
              "upload_date": date.today(),
              "last_edit": date.today(),
              "filter": False,        
              "size": file_info.file_size, 
              "type": message.document.file_name.split('.')[-1],
              "chat_id": chat_id
              }
    #print(file_i)
    reply, reply_type = manager.handle_message(file_i, chat_id, True)
    handle_message(chat_id, reply, reply_type)
    #manager.save_file(file_i)

def handle_file(file):
    pass

def handle_message(chat_id, reply, reply_type):
    if reply_type == ReplyType.multi:
        for i, j in reply:
            handle_message(chat_id, i, j)
    elif reply_type == ReplyType.text:
        send_message(chat_id, reply)
    elif reply_type == ReplyType.photo:
        try:
            bot.send_chat_action(chat_id, "upload_photo")
            photo = open(reply, 'rb')
            send_photo(chat_id, photo)
        except Exception as e: 
            print(e)
    elif reply_type == ReplyType.video:
        send_video(chat_id, reply)

def send_message(chat_id, message):
    #bot.reply_to(msg, reply)
    bot.send_message(chat_id, message, parse_mode="html")

def send_photo(chat_id, photo):
    bot.send_photo(chat_id, photo)

def send_video(chat_id, video):
    bot.send_video(chat_id, video)

def start_bot():
    bot.polling()
