import NLP.execution as execution
import NLP.dialog as dialogs
from Enums.bot_state_enum import BotState as b_state
from Enums.reply_enum import ReplyType
import Globals
import NLP.HelperFunctions as h_functions
import NLP.ExecutionObjects as ExecutionObjects

e_objects = ExecutionObjects.objects
current_file = None
prev_intent = None

def handle_message(msg, chat_id, is_file):
    bot_state = Globals.get_bot_state()
    if is_file:
        if bot_state == b_state.Idle or bot_state == b_state.Waiting_for_file:
            global current_file
            current_file = msg
            Globals.set_bot_state(b_state.Replacing_file)
            file_type = 'log' if current_file['type'] == 'xes' else 'model'
            return f"Thanks for the {file_type}. Would you like me to replace the current {file_type} in the chat with this one?", ReplyType.text
        else:
            return "I'm Sorry, but I'm currently in the middle of something else, please try again later."
    else:        
        if (bot_state == b_state.Mining):
            return ["Sorry but I'm busy right now. Try again later", ReplyType.text]
        elif msg == 'Abort':
            Globals.set_bot_state(bot_state.Idle)
            prev_intent = None
        elif bot_state == b_state.Waiting_for_filter_input:
            reply, reply_type = h_functions.choose_activities(msg, chat_id)
        elif bot_state == b_state.Waiting_for_conformance_input:
            reply, reply_type = execution.handle_conformance(msg, chat_id)
        elif bot_state == b_state.Replacing_file:
            intent = dialogs.askGoogle(msg)
            if current_file == None: 
                return "I'm sorry, something seems to have gone wrong. Please try again.", ReplyType.text
            else:
                reply, reply_type = execution.handle_file_replacement(current_file, intent)
            current_file = None
            Globals.set_bot_state(b_state.Idle)
        elif (msg.startswith('/')):
            #Branch for direct commands
            reply, reply_type = execution.execute_input(msg[1:].lower(), e_objects, chat_id, True)
        else:
            intent = dialogs.askGoogle(msg)
            reply, reply_type = execution.execute_input(intent, e_objects, chat_id, False)

        return reply, reply_type


def save_file(file):
    manager = Globals.get_context_manager()
    manager.save_file(file)