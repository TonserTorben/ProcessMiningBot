import os
import Globals
import PM.pm as pm
import PM.rexecutor as r_executor
from Enums.reply_enum import ReplyType
from Enums.bot_state_enum import BotState
from Enums.execution_enum import ExecutionState
#from ContextManager.ContextManager import ContextManager as c_manager

from decouple import config

R_SCRIPT = config('R_SCRIPT')
R_SCRIPT_FOLDER = config('R_SCRIPT_FOLDER')
ConnectionString = config('CONNECTIONSTRING')
_bot_state = BotState.Idle
_chosen_activities = []

context_manager = Globals.get_context_manager()

def get_bot_state():
    return _bot_state

def bot_start_mining():
    global _bot_state 
    _bot_state = BotState.Mining

def bot_fininsh_mining():
    global _bot_state 
    _bot_state = BotState.Idle

def set_bot_state(bot_state):
    global _bot_state
    _bot_state = bot_state

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
        reply = ['The current log is named: ' + context_manager.get_current_log_name(), ReplyType.text]
    elif choice == 4: #CurrentModel
        reply = ['The current model is named: ' + context_manager.get_current_model_name(), ReplyType.text]
    elif choice == 5: #describelog
        reply = "get_log_description(context_manager._backup)", ReplyType.text
    elif choice == 6: #dfg
        reply = [pm.do_dfg(context_manager.get_current_log(), False), ReplyType.photo]
    elif choice == 7: #dfg_perf
        reply = [pm.do_dfg(context_manager.get_current_log(), True), ReplyType.photo]
    elif choice == 8: #dottedchart
        reply = [r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'dottedchart.R', context_manager.get_current_log()), ReplyType.photo]
    elif choice == 9: #filter
        reply = ['Ok, which activities do you want to keep? \n' \
                 'You can either tell me by writing the names of the activities or giving me the number of the activity \n' \
                 'Please separate the activities by a comma. \n' \
                 "Just write 'Done' when you want me to do the filtering, or 'Stop' if you want to abort \n" \
                 'The activities in the current log are: \n' +
                 list_activities(context_manager.get_current_log()), ReplyType.text]
        set_bot_state(BotState.Waiting_for_filter_input)
    elif choice == 10: # help
        reply = [get_help_text(), ReplyType.text]
    elif choice == 11: #precedencematrix
        bot_start_mining()
        print("begin")
        reply = [r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'precedence_matrix.R', context_manager.get_current_log()), ReplyType.photo]
        bot_fininsh_mining()
        print("end")
    elif choice == 12: #relativedottedchart
        reply = [r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'relative_dotted_chart.R', context_manager.get_current_log()), ReplyType.photo]
    elif choice == 13: #resources
        reply = [r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'resource_frequencies.R', context_manager.get_current_log()), ReplyType.photo]
    else: 
        reply = ["I'm sorry, but I don't understand that command, please type /help to get info on the possible commands.", ReplyType.text]
    return reply

def find_command_back(msg):
    for i in e_obj.objects:
        if i.intent == msg:
            if i.execution == ExecutionState.Nothing:
                return i.function(), i.reply_type
            return i.function, i.reply_type
    return ["I'm sorry, but I don't understand that command, please type /help to get info on the possible commands.", ReplyType.text]

#Used for filtering
def list_activities(log):
    list_of_activities = pm.get_activities(log)
    activities_string = ""
    for i in range (0, len(list_of_activities)):
        activities_string += str(i+1) + ": " + list_of_activities[i] + '\n'
    '''
    for index, activity in enumerate(list_of_activities, start=1):
        activities_string += str(index) + ": " + activity + '\n'
    '''
    return activities_string

#Used for filtering
def choose_activities(msg):
    global _chosen_activities
    if msg.lower() == "done":
        bot_start_mining()
        filtered_log = pm.filter_keep_activities(context_manager.get_current_log(), _chosen_activities)
        _chosen_activities = []
        bot_fininsh_mining()
        context_manager.set_current_log(filtered_log)
        return "The filter has been applied to the file, and the filtered file has been set as the current log.", ReplyType.text
    if msg.lower() == 'stop':
        set_bot_state(BotState.Idle)
        _chosen_activities = []
        return "Ok, I will drop the filtering. Anything else I can help with?", ReplyType.text
    else:
        activities = list(msg.split(","))
        activities = list(map(lambda x: x.strip(), activities))
        print("activities: ", activities)
        #Gets all activities for the current log
        list_of_activities = pm.get_activities(context_manager.get_current_log())
        #Converts all texts to lowercase to make input case insensitive
        list_to_lower =  list(map(lambda x : x.lower(), list_of_activities))
        #Makes a list of all ints in msg
        chosen_ints = list(filter(lambda x : x.isdigit() and int(x)-1 in range(len(list_of_activities)), activities))
        print("Chosen ints: ", chosen_ints)
        #Makes a list of all activities in msg
        chosen_strings = list(filter(lambda x: x.lower() in list_to_lower, activities))
        print("Chosen strings: ", chosen_strings)
        print("List to lower: ", list_to_lower)
        if len(chosen_ints) == 0 and len(chosen_strings) == 0:
            return "I'm sorry, I am currently waiting for inputs to use for filtering, but I am not sure I understand your chosen activities. Please write either their name or the number they are assigned to and separate them by a comma.", ReplyType.text
        for i in activities:
            if i.isdigit():
                _chosen_activities.append(list_of_activities[int(i)-1])
            elif i.lower() in list_to_lower:
                index = list_to_lower.index(i)
                _chosen_activities.append(list_of_activities[index])
        print("Chosen activities: ", _chosen_activities)
        return "Thank you, any more activities you want to keep?", ReplyType.text

def get_log_description(log):
    description = pm.log_desciption(context_manager.get_current_log())
    reply = []
    text_desc = "<b>The total amount of traces is: </b>" + str(description['traces']) + '\n'\
                "<b>Frequencies of activities: </b>: \n"
    for i in description['acts_freq']:
        text_desc += ' - ' + i + ': ' + str(description['acts_freq'][i]) + '\n'
    reply.append([text_desc, ReplyType.text])
    reply.append([description['case_duration'], ReplyType.photo])
    reply.append([description['events_over_time'], ReplyType.photo])
    return [reply, ReplyType.multi]
    

def get_help_text():
    help_text = 'I am a bot build to aid you in process mining tasks, you can write directly what you would like me to do,' \
                ' or you could write a specific subject you would like to hear more about e.g. <b>Discovery</b>, <b>conformance checking</b> or <b>filtering</b>. \n' 
    help_command = 'Alternatively you can also write direct commands to me. \n' + get_command_help_text()
    return help_text  + help_command

#Should dynamically populate by e_object List!!!
def get_command_help_text(): 
    return  '<b>Current direct commands are:</b> \n' \
            '<b>/alpha:</b> Does the alpha miner on the current log. \n' \
            '<b>/conform:</b> This is sadly not implemented yet, but should return a conformance checking of the current log and current model. \n' \
            '<b>/currentlog:</b> This shows the name of the current log. \n' \
            '<b>/currentmodel:</b> This shows the name of the current model. \n' \
            '<b>/describelog:</b> Returns general log statistics. \n' \
            '<b>/dfg:</b> Makes the directly follows graph of the current log with frequency as variant. \n' \
            '<b>/dfg_perf:</b> Makes the directly follows graph of the current log with performance as variant. \n' \
            '<b>/dottedchart:</b> Makes a dotted chart for the current log. \n' \
            '<b>/filter:</b> This is also not implemented yet. \n' \
            '<b>/help:</b> Shows the help menu. \n' \
            '<b>/precedencematrix:</b> Makes the precedence matrix for the current log. \n' \
            '<b>/relativedottedchart:</b> Makes a relative dotted chart for the current log. \n' \
            '<b>/resources:</b> Plots usage of resources. \n' 
                

import NLP.ExecutionObjects as e_obj
#Uniform function to handle both commands and intents from dialogflow
#msg is the input, command is a boolean specifying if input is a command
def execute_input(msg, command):
    for i in e_obj.objects:
        if command:
            if i.command == msg:
                return i.function, i.reply_type
        else:
            if i.intent == msg:
                print(i)
                if i.execution == "Execution.Help":
                    print(i.function())
                    print(i)
                    return i.function(), i.reply_type
                return i.function, i.reply_type


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
