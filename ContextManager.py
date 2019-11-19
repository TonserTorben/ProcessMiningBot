import os
import sys

current_model = os.path.join("Files", "log1.xes")
current_log = os.path.join("Files", "firstLog.xes")
file_one = os.path.join("Files", "log1.xes")
#print(current_file, file_one)

def save_file():
    #Saves a file in the system
    pass

def get_file():
    #Returns the requested file
    pass

def list_files():
    #List files, possibly by type / isFiltered / name etc.
    pass

def check_file():
    #Checks if file is well formed. (Right format, size, as expected)
    pass

def get_current_log():
    return current_log

def get_current_model():
    return current_model