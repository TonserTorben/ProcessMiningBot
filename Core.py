import sys
import os 
sys.path.append(os.getcwd())

import NLP.execution as execution
import NLP.dialog as dialog
import IM.IMManager as im_manager
import IM.TelegramManager as telegram_manager
import IM.SlackManager as slack_manager
import ContextManager as context_manager

from decouple import config

def busy():
    pass

def do_mining():
    pass

def file_management():
    pass

#bot = telegram_manager
bot = slack_manager
bot.start_bot()

