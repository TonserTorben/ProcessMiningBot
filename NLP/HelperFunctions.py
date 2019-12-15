import Globals
from Enums.reply_enum import ReplyType
import PM.pm as pm

context_manager = Globals.get_context_manager()
_chosen_activities = []

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
def choose_activities(msg, chat_id):
    global _chosen_activities
    if msg.lower() == "done":
        Globals.bot_state_init_mining()
        filtered_log = pm.filter_keep_activities(context_manager.get_current_log(chat_id), _chosen_activities)
        _chosen_activities = []
        Globals.bot_state_finish()
        #context_manager.set_current_log(filtered_log)
        return "The filter has been applied to the file, and the filtered file has been set as the current log.", ReplyType.text
    if msg.lower() == 'stop':
        Globals.bot_state_finish()
        _chosen_activities = []
        return "Ok, I will drop the filtering. Anything else I can help with?", ReplyType.text
    else:
        activities = list(msg.split(","))
        activities = list(map(lambda x: x.strip(), activities))
        print("activities: ", activities)
        #Gets all activities for the current log
        list_of_activities = pm.get_activities(context_manager.get_current_log(chat_id))
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

def get_log_description(chat_id):
    description = pm.log_desciption(context_manager.get_current_log(chat_id))
    reply = []
    text_desc = "<b>The total amount of traces is: </b>" + str(description['traces']) + '\n'\
                "<b>Frequencies of activities: </b>: \n"
    for i in description['acts_freq']:
        text_desc += ' - ' + i + ': ' + str(description['acts_freq'][i]) + '\n'
    reply.append([text_desc, ReplyType.text])
    reply.append([description['case_duration'], ReplyType.photo])
    reply.append([description['events_over_time'], ReplyType.photo])
    return reply
    

def get_help_text():
    help_text = 'I am a bot build to aid you in process mining tasks, you can write directly what you would like me to do,' \
                ' or you could write a specific subject you would like to hear more about e.g. <b>Discovery</b>, <b>conformance checking</b> or <b>filtering</b>. \n' 
    help_command = 'Alternatively you can also write direct commands to me. \n' + get_command_help_text()
    return help_text  + help_command

def get_command_help_text():
    from NLP import ExecutionObjects
    e_objects = ExecutionObjects.objects
    help_text = "<b>Currently available direct commands are:</b> \n"
    for i in e_objects: 
        if i.command_help is not None:
            help_text += "<b>" + i.command + ":</b> " + i.command_help + "\n"
    help_text += "All commands will be executed using the current log and or model for the chat."
    return help_text

def list_files():
    pass
