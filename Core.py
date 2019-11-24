import sys
import os 
sys.path.append(os.getcwd())

import NLP.execution as execution
import NLP.dialog as dialog
import IM.IMManager as im_manager
import IM.TelegramManager as telegram_manager
import IM.SlackManager as slack_manager
from ContextManager.ContextManager import ContextManager as context_manager
import Globals

from decouple import config

CONNECTIONSTRING = config('CONNECTIONSTRING')

def busy():
    pass

def do_mining():
    pass

def file_management():
    pass

#g = Globals()
Globals.init_context_manager(CONNECTIONSTRING)

bot = telegram_manager
#bot = slack_manager
bot.start_bot()

#c_manager = context_manager(CONNECTIONSTRING)
#c_manager.init_db()