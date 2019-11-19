import os
from IM.reply_enum import ReplyType
import NLP.execution as execution
from PM import pm
import ContextManager as context_manager
from PM import rexecutor as r_executor
from decouple import config

R_SCRIPT = config('R_SCRIPT')
R_SCRIPT_FOLDER = config('R_SCRIPT_FOLDER')

photo = r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'precedence_matrix.R', context_manager.get_current_log())

'''
Still executes the commands
class Command:
    def __init__(self, title, help_text, execution):
        self.title = title
        self.help_text = help_text
        self.execution = execution

c1 = Command("alpha","Does the alpha miner on the current log.", pm.do_alpha_miner(context_manager.get_current_log()))
c2 = Command("dfg", "Makes the directly follows graph of the current log with frequency as variant.", pm.do_dfg(context_manager.get_current_log(), False))
c3 = Command("dottedchart", 'Makes a dotted chart for the current log.',r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'dottedchart.R', context_manager.get_current_log()))

commandList = [c1, c2]

commandList.append(c3)

for i in commandList:
    print(i.title)
    if i.title == 'alpha':
        print("true")
'''