import os
import sys
from ContextManager.DB_Handler import DB_Handler as db_handler
import tempfile
import hashlib

#print(current_file, file_one)
class ContextManager:
    #Initializer function
    def __init__(self, connection_string, files_folder, hash_block_size):
        self.db = db_handler(connection_string)
        self.files_folder = files_folder
        self.hash_block_size = hash_block_size # Insert into config
        self._current_model = os.path.join("Files", "Petrinet_test_1.pnml")
        self._current_log = os.path.join("Files", "firstLog.xes")
        self._backup = os.path.join("Files", "log1.xes")

    #Initialize the database
    def init_db(self):
        self.db.init_db()
    
    '''
    #Single function to convert files to binaries
    def convert_file_to_binary(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    '''

    # Computing hash of files for comparison in database
    def compute_hash(self, file):
        #Blocksize = 65536
        Blocksize = int(self.hash_block_size)
        sha_hasher = hashlib.sha256()
        with open(file, 'rb') as f:
            buf = f.read(Blocksize)
            while len(buf) > 0: 
                sha_hasher.update(buf)
                buf = f.read(Blocksize)
        print(sha_hasher.hexdigest())
        return sha_hasher.hexdigest()

    #function for comparing hashes from database
    def check_hash(self, file_name):
        # Checks for occurance of hash in db
        #Compute Hash
        file_hash = self.compute_hash(file_name)
        #Check DB for Hash
        db_select = 'Id'
        db_from = 'Files'
        db_where = "Hash = '" + file_hash + "'"
        result = self.db.get_item(db_select, db_from, db_where)
        return file_hash, result


    #Saves file to the database
    #Saves a file in the system
    def save_file(self, file):
        #Write file to temporary file
        _, file_name = tempfile.mkstemp()
        with open(file_name, 'wb') as f:
            f.write(file['file'].content)
        #Check hash of file
        file_hash, existing_file = self.check_hash(file_name)
        if existing_file == None:
            #Save file if no collision in hash is detected
            file_path = self.files_folder + file['name']
            with open (file_path, 'wb') as f:
                f.write(file['file'].content)
            return False, self.db.insert_file(file_hash, file['chat_id'], file['user'], file['upload_date'], file['name'], path=file_path, size=file['size'], type=file['type'])
        else: 
            #Collision in hash is detected. Save file by reference to existing file
            return True, self.db.insert_file(file_hash, file['chat_id'], file['user'], file['upload_date'], file['name'], file_id=existing_file)
        

    def get_file(self, file_id):
        #Returns the requested file
        db_select = "Id, Name"
        db_from = "Files"
        db_where = "Id = " + str(file_id)
        return self.db.get_item(db_select, db_from, db_where)

    #Skal denne bruges?
    def update_file(self, file):
        pass

    #Listing files should contain functions: List_all_file_in_chat list_my_files list_log_in_chat list_models_in_chat
    def list_chat_files(self, chat_id):
        #List files, possibly by type / isFiltered / name etc. e.g. list files for this chat of list my uploaded files. 
        # The Second argument of get_items should be dynamic in order for the output to be shifted.
        db_select = "f.Id, fc.File_name, fc.User, fc.Upload_date, f.Size, f.Type" #fc.Filtered
        db_from = "Files as f join Files_in_Chat as fc on f.Id = fc.File_id"
        db_where = "fc.Chat_id = " + str(chat_id)
        result = self.db.get_items(db_select, db_from, db_where)
        #print(result)
        if result == None:
            return "There are no files associated with this chat currently."
        result_string = ""
        for i, n, u, d, s, t in result:
            # i = Id, n = Name, u = User, d = upload date, s = Size, t = Type
            # Detailed Result_string
            # result_string += "ID: " + str(i) + ", Name: " + n + ", User: " + u + ", Date of Upload: " + str(d) + ", Size: " + str(s) + ", Type: " + t + "\n"
            result_string += "<b>ID: </b>" + str(i) + ", <b>Name: </b>" + n + ", <b>Size: </b>" + s + ", <b>Type: </b>" + t + "\n"
        return result_string[:-1]
        

    def check_file(self):
        #Checks if file is well formed. (Right format e.g. model type .pnml or log type .xes, size, as expected)
        pass
    
    #Gets the current document e.g. log or model for a specific chat
    def get_current_file(self, chat_id, doc_type):
        db_select = "f.File_path"
        db_from = "Files as f join Files_in_Chat as fc on f.Id = fc.File_id join Current_file as cf on fc.Id = cf.File_id"
        db_where = "cf.Chat_id = '" + str(chat_id) + "' and cf.type = '" + doc_type + "'"
        current_log = self.db.get_item(db_select, db_from, db_where)
        return current_log
    
    #Gets the current document name for a document e.g. log or model for a specific chat
    def get_current_file_name(self, chat_id, doc_type):
        '''db_select = "f.File_name"
        db_from = "Files_in_chat as f join Current_File as cf on f.File_id = cf.File_id"
        db_where = "cf.Chat_id = '" + chat_id + "' and cf.type = " + doc_type
        current_name = self.db.get_item(db_select, db_from, db_where)
        return current_name'''
        db_select = "f.File_name"
        db_from = "Files_in_chat as f join Current_file as cf on f.Id = cf.File_id"
        db_where = "cf.Chat_id = " + str(chat_id) + " and cf.type = 'xes'"
        current_name = self.db.get_item(db_select, db_from, db_where)
        if current_name == None:
            return "There is no current log in this chat"
        return current_name

    #Sets the current document e.g. log or model for a specific chat
    def set_current_file(self, file_id, file):
        # Check if there is a current file in the chat
        db_select = 'Id'
        db_from = 'Current_file'
        db_where = "Chat_id = '" + str(file['chat_id']) + "' and Type = '" + file['type'] + "'"
        if self.db.get_item(db_select, db_from, db_where) == None:
            self.db.insert_current_file(file, file_id)
        else:
            db_update = "Current_File"
            db_set = "File_id = " + str(file_id) #file_id is reference to the documents in files_in_chat. Doc_id er reference til dokumentets reference i files_in_chat
            db_where = "type = '" + file['type'] + "' and Chat_id = '" + str(file['chat_id']) + "'"
            self.db.update_item(db_update, db_set, db_where)

    # Uploads a new document to the Table Files, Sets Reference in the Files_in_chat and possibly in the Filtered_files if the file is filtered
    def upload_file(self, file, chat, type,  is_filtered):
        #Upload fil, sæt reference i files_in_chat, hvis det er en filtreret fil skal dette også opsættes i Filtered_files
        pass

    def get_script(self, name):
        db_select = "Name, Language, Script, Output"
        db_from = "Scripts"
        db_where = "Name = '" + name + "'"
        script = self.db.get_item(db_select, db_from, db_where)
        return script

    def save_script(self, name, language, script, output):
        db_values = {'name': name, 'language': language, 'script': script, 'output': output}
        self.db.insert_script(db_values)
    #Definer Rename_file?

#Set og Get-log name/file skal bruge current_file_in_chaT TABEL

    #ALT HERUNDER SKAL SLETTES!!!
    def get_current_log(self, chat_id):
        db_select = "f.File_path"
        db_from = "Files as f join Files_in_Chat as fc on f.Id = fc.File_id join Current_file as cf on fc.Id = cf.File_id"
        db_where = "cf.Chat_id = '" + str(chat_id) + "' and cf.type = 'xes'"
        current_log = self.db.get_item(db_select, db_from, db_where)
        print(current_log)
        return current_log

    def get_current_log_name(self, chat_id):
        db_select = "f.File_name"
        db_from = "Files_in_chat as f join Current_file as cf on f.Id = cf.File_id"
        db_where = "cf.Chat_id = " + str(chat_id) + " and cf.type = 'xes'"
        current_log = self.db.get_item(db_select, db_from, db_where)
        if current_log == None:
            return "There is no current log in this chat"
        return current_log

    def get_current_model(self, chat_id):
        db_select = "f.Path"
        db_from = "Files as f join Current_file as cf on f.Id = cf.File_id"
        db_where = "cf.Chat_id = " + str(chat_id) + " and cf.type = 'pnml'"
        current_model = self.db.get_item(db_select, db_from, db_where)
        return current_model

    def get_current_model_name(self, chat_id):
        db_select = "f.File_name"
        db_from = "Files_in_chat as f join Current_file as cf on f.Id = cf.File_id"
        db_where = "cf.Chat_id = " + str(chat_id) + " and cf.type = 'pnml'"
        current_model = self.db.get_item(db_select, db_from, db_where)
        if current_model == None:
            return "There is no current model in this chat."
        return current_model