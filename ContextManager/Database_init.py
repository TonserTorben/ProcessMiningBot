import sqlite3

class DB_Creation:

    create_file_table = "CREATE TABLE IF NOT EXISTS Files(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, File BLOB, User TEXT, Date_of_upload DATE, Last_Edited DATE, Filtered BOOLEAN, Size TEXT, Type TEXT);" 
    # Name = name of file, File = The file itself, User = the name of the user who uploaded it, Date_of_upload = The date the file was uploaded, Last_edited = The time of the last edit, Filtered = If this is a filtered file or not (Might be omitted), Size = the size of the file, Type = the type of the file e.g. .xes or .pnml or others
    create_Scripts_table = "CREATE TABLE IF NOT EXISTS Scripts(Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Language TEXT, Script Text, Output TEXT);" 
    # Name = Name of script e.g. dottedchart.R, Language = language of script e.g. R, Script = the contents of the script itself, Output = what can be expected from this script e.g. photo or text (Might be omitted)
    create_filter_types_table = "CREATE TABLE IF NOT EXISTS Filter_Types(Id INTEGER PRIMARY KEY AUTOINCREMENT, Type TEXT);"
    # Used as reference for the Filtered_Files Table. Type = the type of filter applied to this file e.g. keep_acitivity or other.
    create_filtered_file_table = "CREATE TABLE IF NOT EXISTS Filtered_Files(Id INTEGER PRIMARY KEY AUTOINCREMENT, Original_id INT, Filtered_id INT, Filter_type INT,  FOREIGN KEY(Original_id) REFERENCES Files(Id), FOREIGN KEY(Filtered_id) REFERENCES Files(Id) ON DELETE CASCADE, FOREIGN KEY(Filter_type) REFERENCES Filter_Types(Id));"
    # Used to note which files has been filtered and where these files originated from. Original_id = The id of the original unfiltered file, Filtered_id = the id of the file that has been filtered, Filter_type = the type of filter that has been applied to this file.
    # Kan muligvis indeholde parametre for filtrering e.g. hvilke aktiviteter der er beholdt.
    create_files_in_chat_table = "CREATE TABLE IF NOT EXISTS Files_in_Chat(Id INTEGER PRIMARY KEY AUTOINCREMENT, Chat_id TEXT, File_id);"
    # Used to keep track of which files are in which chat. 
    create_current_file_table = "CREATE TABLE IF NOT EXISTS Current_file(Id INTEGER PRIMARY KEY AUTOINCREMENT, Chat_id TEXT, File_id INT, Type TEXT, FOREIGN KEY(File_id) REFERENCES Files(Id) ON DELETE CASCADE);"
    # Used to keep track of the current files in a given chat. Chat_id = the Id of the chat, Platform = which platform the chat is on e.g. Slack or Telegram (Might be omitted), File_id = the id of the file, Type = The type of the file e.g. Log or Model (Since each chat could have one current log and one current model)
    sql = []

    def __init__(self, db):
        self.db = db
        self.c = self.db.cursor()
        statements = [self.create_file_table, self.create_Scripts_table, self.create_filter_types_table, self.create_filtered_file_table, self.create_files_in_chat_table, self.create_current_file_table]
        self.sql = statements

    def close(self):
        self.db.close()

    #TODO Create a Msg_Table to store messages, in order to send messages across platforms.

    def create_tables(self):
        for i in self.sql:
            self.c.execute(i)
            self.db.commit()

