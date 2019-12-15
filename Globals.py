from Enums.bot_state_enum import BotState
from Enums.reply_enum import ReplyType
from Enums.execution_enum import ExecutionState

from ContextManager.ContextManager import ContextManager
#Should contain all global variables e.g. 
from decouple import config

CONNECTIONSTRING = config('CONNECTIONSTRING')
FILES_FOLDER = config('FILES_FOLDER')
HASH_BLOCK_SIZE = config('HASH_BLOCK_SIZE')
R_SCRIPT = config('R_SCRIPT')

_botstate = BotState.Idle
_execution_state = ExecutionState.Nothing
_context_manager = ContextManager(CONNECTIONSTRING, FILES_FOLDER, HASH_BLOCK_SIZE)

def get_bot_state():
    return _botstate

def set_bot_state(botstate):
    global _botstate
    _botstate = botstate

def bot_state_init_mining():
    global _botstate
    _botstate = BotState.Mining

def bot_state_finish():
    global _botstate
    _botstate = BotState.Idle

def get_execution_state():
    return _execution_state

def set_execution_state(state):
    global _execution_state
    _execution_state = state

def init_context_manager(connection_string, files_folder, hash_block_size):
    global _context_manager
    _context_manager = ContextManager(connection_string, files_folder, hash_block_size)

def get_context_manager():
    return _context_manager

def set_context_manager(connectionstring):
    pass

def get_r_script():
    return R_SCRIPT
