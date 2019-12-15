import os
import Globals
import PM.pm as pm
import PM.rexecutor as r_executor
from Enums.reply_enum import ReplyType
from Enums.bot_state_enum import BotState
from Enums.execution_enum import ExecutionState
#from ContextManager.ContextManager import ContextManager as c_manager
from NLP import HelperFunctions as h_functions

from decouple import config

R_SCRIPT = config('R_SCRIPT')
R_SCRIPT_FOLDER = config('R_SCRIPT_FOLDER')

_previous_intent = None

def find_command_back(msg, e_obj):
    for i in e_obj.objects:
        if i.intent == msg:
            if i.execution == ExecutionState.Nothing:
                return i.function(), i.reply_type
            return i.function, i.reply_type
    return ["I'm sorry, but I don't understand that command, please type /help to get info on the possible commands.", ReplyType.text]


#import NLP.ExecutionObjects as e_obj
#Uniform function to handle both commands and intents from dialogflow
#msg is the input, command is a boolean specifying if input is a command
def execute_input(msg, e_objects, chat_id, command):
    global _previous_intent
    context_manager = Globals.get_context_manager()
    function = None
    reply_type = None
    for i in e_objects: # !!!!!!!
        if command:
            if i.command is not None and i.command[1:] == msg:
                function = i.function
                reply_type = i.reply_type
                _previous_intent = i
                break
        else:
            if i.intent == msg:
                function = i.function
                reply_type = i.reply_type
                _previous_intent = i
                break
    if function == None or reply_type == None:
        return ["I'm sorry, but I don't understand that command, please type /help to get info on the possible commands.", ReplyType.text]
    if i.change_state:
        if i.new_state == BotState.Waiting_for_conformance_input:
            Globals.set_bot_state(BotState.Waiting_for_conformance_input)
            return """How would you like the conformance check to be done? by running alpha miner on the current log and using this for model, by running inductive miner on the current log and using this for model or just by using the current model?\n
Please write 'alpha', 'inductive' or 'current' to choose an option.""", reply_type.text
    if i.script_from_db:
        #Import script to run
        _, _, script, _ = context_manager.get_script(i.script_name)
        Globals.bot_state_init_mining()
        result = i.function(script, context_manager.get_current_log(chat_id))
        Globals.bot_state_finish()
        return result, i.reply_type
    if i.execution == ExecutionState.Nothing:
        #function doesn't take any arguments
        return function(), reply_type
    elif i.execution == ExecutionState.Log:
        #Function takes log as argument
        Globals.bot_state_init_mining()
        result = function(context_manager.get_current_file(chat_id, 'xes'))
        Globals.bot_state_finish()
        return result, reply_type
    elif i.execution == ExecutionState.Model:
        #Function takes model as argument
        Globals.bot_state_init_mining()
        result = function(context_manager.get_current_model(chat_id))
        Globals.bot_state_finish()
        return result, reply_type
    elif i.execution == ExecutionState.Both:
        #Funtion takes both log and model as argument
        Globals.bot_state_init_mining()
        result = function(context_manager.get_current_log(chat_id), context_manager.get_current_model(chat_id)), reply_type
        Globals.bot_state_finish()
        return result, reply_type
    elif i.execution == ExecutionState.Chat_id:
        result = function(chat_id)
        return result, reply_type
    else: 
        return function, reply_type
    

def handle_conformance(msg, chat_id):
    c_manager = Globals.get_context_manager()
    conformance_type = ""
    conformance_model = ""
    if 'precision' in _previous_intent.intent:
        conformance_type = 'precision'
    elif 'fitness' in _previous_intent.intent:
        conformance_type = 'fitness'
    elif 'complete' in _previous_intent.intent:
        conformance_type = 'complete'
    else:
        return "Somethings wrong", ReplyType.text
    if msg.lower() == 'alpha':
        conformance_model = 'alpha'
    elif msg.lower() == 'inductive':
        conformance_model = 'inductive'
    elif msg.lower() == 'current':
        conformance_model = 'current'
    else:
        return "somethings wrong with your input", ReplyType.text

    Globals.bot_state_init_mining()
    print(_previous_intent.function)
    result = _previous_intent.function(c_manager.get_current_log(chat_id), c_manager.get_current_model(chat_id), conformance_type, conformance_model)
    info = result['result']
    result_string = ""
    if(isinstance(info, dict)):
        for key, value in info.items(): 
            result_string += key + ": " + str(value) + "\n"
    else:
        result_string = conformance_type + "_" + conformance_model + " = " + str(info)
    reply = [[[result_string[:-1], ReplyType.text], [result['Model'], ReplyType.photo]], ReplyType.multi]
    print("result: ", result)
    Globals.bot_state_finish()
    return reply
    
def handle_file_replacement(current_file, intent):
    c_manager = Globals.get_context_manager()
    file_type = 'log' if current_file['type'] == 'xes' else 'model'
    existing, last_id = c_manager.save_file(current_file)
    if intent == 'Yes':
        c_manager.set_current_file(last_id, current_file)
        reply = f"Ok I've uploaded the {file_type} and replaced it as the chats current {file_type}"
    elif intent == 'No':
        reply = f"Ok I haven't replaced the current {file_type}. I've just saved the {file_type} you sent me to this chats files."
    if existing: 
        return [[reply, ReplyType.text], ["FUY. The file you've uploaded, seems to already exist on the server so I've created a reference to that file in stead.", ReplyType.text]], ReplyType.multi
    return reply, ReplyType.text
