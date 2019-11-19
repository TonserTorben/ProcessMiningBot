import os
import PM.pm as pm
import PM.rexecutor as r_executor
from IM.reply_enum import ReplyType
import ContextManager as context_manager

from decouple import config

R_SCRIPT = config('R_SCRIPT')
R_SCRIPT_FOLDER = config('R_SCRIPT_FOLDER')


waiting_for_file = True
print(os.path)

def findAnswer(answer):
    if answer in answers: 
        result = answers[answer]
        if isinstance(result, int): 
            return execute_command(result)
        else: 
            return [result, ReplyType.text]
    else: 
        return ["Sorry, I'm not sure I understand that message.", ReplyType.text]

def find_command(msg):
    switcher = {'alpha': 1,
                'conform': 2,
                'currentlog': 3,
                'currentmodel': 4, 
                'describelog': 5, 
                'dfg': 6,
                'dfg_perf': 7,
                'dottedchart': 8,
                'filter': 9,
                'help': 10,
                'precedencematrix': 11,
                'relativedottedchart': 12, 
                'resources': 13
    }
    return execute_command(switcher.get(msg, 0))

# Move to execution
def execute_command(choice):
    if   choice == 1: #Alpha
        reply = [pm.do_alpha_miner(context_manager.get_current_log()), ReplyType.photo]
    elif choice == 2: #Conformance
        reply = ['Not Implemented yet!', ReplyType.text]
    elif choice == 3: #CurrentLog
        reply = ['The current log is named: ' + context_manager.get_current_log(), ReplyType.text]
    elif choice == 4: #CurrentModel
        reply = ['The current model is named: ' + context_manager.get_current_model(), ReplyType.text]
    elif choice == 5: #describelog
        reply = ["this should be able to send multiple messages. Not Implemented yet!", ReplyType.text]
    elif choice == 6: #dfg
        reply = [pm.do_dfg(context_manager.get_current_log(), False), ReplyType.photo]
    elif choice == 7: #dfg_perf
        reply = [pm.do_dfg(context_manager.get_current_log(), True), ReplyType.photo]
    elif choice == 8: #dottedchart
        reply = [r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'dottedchart.R', context_manager.get_current_log()), ReplyType.photo]
    elif choice == 9: #filter
        reply = ['Not Implemented yet!', ReplyType.text]
    elif choice == 10: # help
        reply = [get_help_text(), ReplyType.text]
    elif choice == 11: #precedencematrix
        reply = [r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'precedence_matrix.R', context_manager.get_current_log()), ReplyType.photo]
    elif choice == 12: #relativedottedchart
        reply = [r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'relative_dotted_chart.R', context_manager.get_current_log()), ReplyType.photo]
    elif choice == 13: #resources
        reply = [r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'resource_frequencies.R', context_manager.get_current_log()), ReplyType.photo]
    else: 
        reply = ["I'm sorry, but I don't understand that command, please type /help to get info on the possible commands.", ReplyType.text]
    return reply

def get_help_text():
    help_text = 'I am a bot build to aid you in process mining tasks, you can write directly what you would like me to do, or you could write a specific subject you would like to hear more about e.g. <b>Discovery</b>, <b>conformance checking</b> or <b>filtering</b>. \n ' 
    help_command = 'Alternatively you can also write direct commands to me. \n' + get_command_help_text()[0]
    return help_text  + help_command

def get_command_help_text():
    return ['<b>Current direct commands are:</b> \n ' +
                '<b>/alpha:</b> Does the alpha miner on the current log. \n ' + 
                '<b>/conform:</b> This is sadly not implemented yet, but should return a conformance checking of the current log and current model. \n ' + 
                '<b>/currentlog:</b> This shows the name of the current log. \n' + 
                '<b>/currentmodel:</b> This shows the name of the current model. \n' +
                '<b>/describelog:</b> Returns general log statistics. \n ' + 
                '<b>/dfg:</b> Makes the directly follows graph of the current log with frequency as variant. \n ' +
                '<b>/dfg_perf:</b> Makes the directly follows graph of the current log with performance as variant. \n ' +
                '<b>/dottedchart:</b> Makes a dotted chart for the current log. \n ' + 
                '<b>/filter:</b> This is also not implemented yet. \n' + 
                '<b>/help:</b> Shows the help menu. \n' +
                '<b>/precedencematrix:</b> Makes the precedence matrix for the current log. \n ' +
                '<b>/relativedottedchart:</b> Makes a relative dotted chart for the current log. \n ' +
                '<b>/resources:</b> Plots usage of resources. \n '
                , ReplyType.text]


answers = { 'Alpha'                         : 1,
            'Conformance'                   : 2,
            'DescribeLog'                   : 5,
            'DFG'                           : "What kind of directly follows graph would you like me to do? Resource or performance?",
            'DFG_performance_follow'        : 7,
            'DFG_resource_follow'           : 6,
            'DFG_performance'               : 7,
            'DFG_resource'                  : 6,
            'Discovery'                     : "Okay, what kind of discovery would you like to perform? \n"
                                                "Currently I support: dfg for frequence or performance, alpha miner, ", 
            'Dottedchart'                   : "What kind of dotted chart would you like me to do? Relative or absolute?",
            'Dottedchart_absolute_follow'   : 8,
            'Dottedchart_relative_follow'   : 12,
            'Dottedchart_absolute'          : 8,
            'Dottedchart_relative'          : 12,
            'Fine'                          : "That's nice to hear!", 
            'Help'                          : get_help_text(),
            'HowAreYou'                     : 'I am fine and you?', 
            'PrecedenceMatrix'              : 11,
            'Sad'                           : "I'm sorry to hear that. What's the problem?",
            'Show_resources'                : 13,
            'Welcome'                       : 'Hi user! nice to meet you!', 
            #add confirm?
            # Maybe add ReplyType for the replies?
        }

'''answers_including_choices = { 'Alpha'                         : "Okay. would you like me to perform this on the current log, or would you like to upload a new log file?",
            'Conformance'                   : "Not implemented yet!",
            'DescribeLog'                   : "Not implemented yet!",
            'DFG'                           : "Not implemented yet!",
            'DFG_resource_follow'           : "Not implemented yet!",
            'DFG_performance_follow'        : "Not implemented yet!",
            'DFG_performance'               : "Not implemented yet!",
            'DFG_resource'                  : "Not implemented yet!",
            'Discovery'                     : "Okay, what kind of discovery would you like to perform? \n"
                                                "Currently I support: dfg for frequence or performance, alpha miner, ", 
            'Dottedchart'                   : "Not implemented yet!",
            'Dottedchart_absolute_follow'   : "Not implemented yet!",
            'Dottedchart_relative_follow'   : "Not implemented yet!",
            'Dottedchart_absolute'          : "Not implemented yet!",
            'Dottedchart_relative'          : "Not implemented yet!",
            'Fine'                          : "That's nice to hear!", 
            'Help'                          : get_help_text(),
            'HowAreYou'                     : 'I am fine and you?', 
            'PrecedenceMatrix'              : "Not implemented yet!",
            'Sad'                           : "I'm sorry to hear that. What's the problem?",
            'Show_resources'                : "Not implemented yet!",
            'Welcome'                       : 'Hi user! nice to meet you!', 
            #add confirm?
            # Maybe add ReplyType for the replies?
        }
'''