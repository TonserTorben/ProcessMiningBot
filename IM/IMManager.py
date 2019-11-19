import NLP.execution as execution
import NLP.dialog as dialogs

import ContextManager
from IM.reply_enum import ReplyType


def get_intention(msg):
    #reply_type = ReplyType.text
    if (msg.startswith('/')):
        #Branch for direct commands
        reply, reply_type = execution.find_command(msg[1:].lower())
    else:
        intent = dialogs.askGoogle(msg)
        reply, reply_type =  execution.findAnswer(intent)

    return reply, reply_type
