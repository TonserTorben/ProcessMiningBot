import NLP.execution as execution
import NLP.dialog as dialogs
from Enums.bot_state_enum import BotState as bot_state
from Enums.reply_enum import ReplyType
from ContextManager.ContextManager import ContextManager as c_manager
import Globals

def handle_message(msg):
    bot_state = Globals.get_bot_state()
    if (bot_state == bot_state.Mining):
        return ["Sorry but I'm busy right now. Try again later", ReplyType.text]
    elif bot_state == bot_state.Waiting_for_filter_input:
        reply, reply_type = execution.choose_activities(msg)
    elif (msg.startswith('/')):
        #Branch for direct commands
        reply, reply_type = execution.find_command(msg[1:].lower())
    else:
        intent = dialogs.askGoogle(msg)
        #reply, reply_type =  execution.findAnswer(intent)
        reply, reply_type = execution.find_command_back(intent)

    return reply, reply_type

from decouple import config
connectionstring = config('CONNECTIONSTRING')
manager = c_manager(connectionstring)
def save_file(file):
    manager.save_file(file)