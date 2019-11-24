import os
import sys
from ContextManager.DB_Handler import DB_Handler as db_handler
_current_model = os.path.join("Files", "Petrinet_test_1.pnml")
_current_log = os.path.join("Files", "firstLog.xes")
_backup = os.path.join("Files", "log1.xes")
#print(current_file, file_one)
class ContextManager:
    def __init__(self, connectionString):
        self.db = db_handler(connectionString)

    def convert_file_to_binary(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def init_db(self):
        self.db.init_db()

    #Saves file to the database
    def save_file(self, file):
        #Saves a file in the system
        file['file'] = self.convert_file_to_binary(file['file'])
        self.db.insert_file(file)

    def get_file(self, clauses):
        #Returns the requested file
        #SELECT File FROM Files WHERE Name = Filename / Id = file_id
        return self.db.get_item("Files", "File", clauses)

    #Skal denne bruges?
    def update_file(self, file):
        pass

    def list_chat_files(self, clauses):
        #List files, possibly by type / isFiltered / name etc. e.g. list files for this chat of list my uploaded files. 
        # The Second argument of get_items should be dynamic in order for the output to be shifted.
        return self.db.get_items("Files", "Name, Size, User", clauses)
        

    def check_file(self):
        #Checks if file is well formed. (Right format e.g. model type .pnml or log type .xes, size, as expected)
        pass
    
    #Gets the current document e.g. log or model for a specific chat
    def get_current_file(self, chat, doc_type):
        db_select = "f.File"
        db_from = "Files as f join Current_File as cf on f.Id = cf.File_id"
        db_where = "cf.Chat_id = " + chat + " and cf.type = "  + doc_type
        current_log = self.db.get_item(db_select, db_from, db_where)
        return current_log
    
    #Gets the current document name for a document e.g. log or model for a specific chat
    def get_current_file_name(self, chat, doc_type):
        db_select = "f.Name"
        db_from = "Files as f join Current_File as cf on f.Id = cf.File_id"
        db_where = "cf.Chat_id = " + chat + " and cf.type = " + doc_type
        current_name = self.db.get_item(db_select, db_from, db_where)
        return current_name

    #Sets the current document e.g. log or model for a specific chat
    def set_current_file(self, chat, doc_id, doc_type):
        db_update = "Current_File"
        db_set = "File_id = " + doc_id #Doc_id er reference til dokumentets reference i files_in_chat
        db_where = "type = " + doc_type + "and chat_id = " + chat
        self.db.update_item(db_update, db_set, db_where)
        pass

    # Uploads a new document to the Table Files, Sets Reference in the Files_in_chat and possibly in the Filtered_files if the file is filtered
    def upload_file(self, file, chat, type,  is_filtered):
        #Upload fil, sæt reference i files_in_chat, hvis det er en filtreret fil skal dette også opsættes i Filtered_files
        pass

    #Definer Rename_file?


    #ALT HERUNDER SKAL SLETTES!!!
    def get_current_log(self):
        return _current_log

    def get_current_log_name(self):
        return os.path.basename(_current_log)

    def set_current_log(self, log):
        global _current_log
        _current_log = log

    def get_current_model(self):
        return _current_model

    def get_current_model_name(self):
        return os.path.basename(_current_model)

    def set_current_model(self, model):
        global _current_model
        _current_model = model