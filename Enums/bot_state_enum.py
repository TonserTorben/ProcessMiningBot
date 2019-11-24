import enum

class BotState(enum.Enum):
    Idle                            = 1 #Not doing anything
    Waiting_for_filter_input        = 2 #Waiting for input to filter functions
    Waiting_for_choice              = 3 #Waiting for yes/no answer
    Waiting_for_conformance_input   = 4 #
    Waiting_for_file                = 5 #Waiting for the user to send a file
    Listing_files                   = 6 #Listed files for the user
    Mining                          = 7 #Currently working