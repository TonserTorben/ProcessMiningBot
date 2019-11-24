import os
#from IM.reply_enum import ReplyType
#import NLP.execution as execution
#from PM import pm
#import ContextManager as context_manager
#from PM import rexecutor as r_executor
from decouple import config

R_SCRIPT = config('R_SCRIPT')
R_SCRIPT_FOLDER = config('R_SCRIPT_FOLDER')

#photo = r_executor.run_r(R_SCRIPT, R_SCRIPT_FOLDER + 'precedence_matrix.R', context_manager.get_current_log())

from pm4py.objects.log.importer.xes import factory as xes_importer

log_path = os.path.join("Files", "firstLogFresh.xes")
log = xes_importer.import_log(log_path)

from pm4py.util import constants
from pm4py.statistics.traces.log import case_statistics
#try:
#    x, y = case_statistics.get_kde_caseduration(log, parameters={constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"})
#except Exception as e:
#    print (e)

from pm4py.visualization.graphs import factory as graph_vis_factory

#gviz = graph_vis_factory.apply_plot(x, y, variant="cases")
#graph_vis_factory.view(gviz)

'''import telebot

class teletest:
    api = config('TELEGRAM_TOKEN')
    bot = telebot.TeleBot(api)
    def __init__(self):
        self.api = config('TELEGRAM_TOKEN')
    

    #@bot.message_handler(func=lambda message: True)
    def receive_message(self, message):
        self.bot.send_message(self, message.text)

    receive_message = bot.message_handler(func=lambda message: True)(receive_message)

    def start(self):
        self.bot.polling()

bot_test = teletest()
bot_test.start()

import sqlite3
connect = config('CONNECTIONSTRING')
def convertToBinary(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBlob(ids, name, file, user, date, init, filt, size, types):
    try:
        sqliteConnection = sqlite3.connect(connect)
        c = sqliteConnection.cursor()
        print("connected")
        sqlite_insert = """ INSERT INTO Files VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        ids = ids
        name = name
        file = convertToBinary(file)
        user = user
        date = date
        init = init
        filt = filt
        size = size
        types = types

        data_tuple = (ids, name, file, user, date, init, filt, size, types)

        c.execute(sqlite_insert, data_tuple)
        sqliteConnection.commit()
        print("Inserted")
        c.close()

    except sqlite3.Error as Error:
        print("Failed: ", Error)
    finally: 
        if (sqliteConnection):
            sqliteConnection.close()
            print("Closed")

insertBlob(1, "test", "C:\\Users\\Rasmu\\Downloads\\tom-hanks-forrest-gump.jpg", "Rasmus", "2019-11-11", "2019-11-10", False, 123, ".jpg")
'''

import NLP.ExecutionObjects as objects
from Enums.bot_state_enum import BotState
from Enums.reply_enum import ReplyType
from Enums.execution_enum import ExecutionState
from ContextManager.ContextManager import ContextManager as c_manager
from Globals import Globals

def get_help_text():
    h_string = str(map(lambda x: x.command + "\n", objects.objects))
    print(h_string)
    h2_string = ""
    for i in objects.objects:
        if(i.command != ""):
            h2_string += i.command + "\n"
    print(h2_string[:-1])
get_help_text()

con_string = config('CONNECTIONSTRING')
bot = BotState.Idle
context = c_manager(con_string)
g = Globals()
prev_intent = None

def handle_intent(msg):
    for i in objects.objects:
        if i.intent == msg: 
            if i.intent == 'Abort':
                bot = BotState.Idle
                prev_intent  = None
                return "Ok I'll stop what I'm currently doing.", ReplyType.text
            elif i.ask_for_file and bot.botstate == BotState.Idle:
                prev_intent = i
                bot = BotState.Waiting_for_choice
                if i.execution == ExecutionState.Log:
                    return "The name of the current log in the chat is: " + "GetCurrentLog()" + "\n Would you like to use this log?", ReplyType.text
                if i.execution == ExecutionState.Model:
                    return "The name of the current model in the chat is: " + "GetCurrentModel()" + "\n Would you like to use this model?", ReplyType.text
                if i.execution == ExecutionState.Both:
                    return "The name of the current log and model in the chat is: " + "GetCurrentLog(), GetCurrentModel()" + "\n Would you like to use this log and model?", ReplyType.text
            #First check state of bot to determing whether or not e.g. yes/no intents make sense
            elif bot == BotState.Waiting_for_choice:
                if i.intent == 'Yes':
                    log = context.get_current_log()
                    model = context.get_current_model()
                    exe = prev_intent.execution
                    func = prev_intent.function
                    if exe == ExecutionState.Log:
                        bot = BotState.Mining
                        func(log)
                        bot = BotState.Idle
                    elif exe == ExecutionState.Model:
                        bot = BotState.Mining
                        func(model)
                        bot = BotState.Idle
                    elif exe == ExecutionState.Both:
                        bot = BotState.Mining
                        func(log, model)
                        bot = BotState.Idle
                elif i.intent == 'No':
                    bot = BotState.Waiting_for_file
                    return "Which file would you like to use? \n Currently I have access to following files: \n " + "listFiles()" + "\n would you like to use on of these files?"
            elif bot == BotState.Waiting_for_file:
                # Should handle if the user writes a file from the db or sends a new file.
                # Should also handle whether or not both files (log and model) should be given
                pass
            elif bot == BotState.Listing_files:
                pass
            elif bot == BotState.Mining:
                return "I'm currently busy, please wait till I finish doing my task.", ReplyType.text
            #Afterwards check Execution.enum to check whether or not inputs are needed for a possible function
            return