import sqlite3

class DB_Handler:
    
    def __init__(self, connectionString):
        self.db = sqlite3.connect(connectionString, check_same_thread=False)
        self.c = self.db.cursor()

    def close(self):
        self.db.close()

    def get_item(self, db_select, db_from, db_where):
        #Idea is to specify the specific table, what item to get and the clauses for the select statement.
        statement = "SELECT {} FROM {} WHERE {}".format(db_select, db_from, db_where)
        print(statement)
        self.c.execute(statement)
        result = self.c.fetchone()
        result = result[0] if result != None else None
        return result

    def get_items(self, db_select, db_from, db_where):
        statement = "SELECT {} FROM {} WHERE {}".format(db_select, db_from, db_where)
        self.c.execute(statement)
        results = self.c.fetchall()
        return results
        
    #Skal opdateres til hver enkelt tabel
    def update_item(self, db_update, db_set, db_where):
        statement = "UPDATE {} SET {} WHERE {}".format(db_update, db_set, db_where)
        self.c.execute(statement)
        self.db.commit()

    def insert_item(self, db_into, db_values):
        statement = "INSERT INTO {} VALUES {}".format(db_into, db_values)        
        self.c.execute(statement)
        self.db.commit()

    #Insert STATEMENTS
    # Inserting file in both Files table and Files_in_chat table
    def insert_file(self, file_hash, chat_id, user, date, name, file_id=None, path=None, size=None, type=None):
        if file_id == None:
            statement = "INSERT INTO Files (Hash, File_path, Size, Type) Values(?, ?, ?, ?)"
            values = (file_hash, path, size, type)
            self.c.execute(statement, values)
            self.db.commit()
            file_id = self.c.lastrowid
        else:
            file_id = file_id
        statement = "INSERT INTO Files_in_Chat (Chat_id, File_id, User, Upload_date, File_name) VALUES(?, ?, ?, ?, ?)"
        values = (chat_id, file_id, user, date, name)
        self.c.execute(statement, values)
        self.db.commit()
        file_in_chat_id = self.c.lastrowid
        return file_in_chat_id

    def insert_script(self, script):
        statement = "INSERT INTO Scripts (Name, Language, Script, Output) VALUES(?, ?, ?, ?)"
        values = (script['name'], script['language'], script['script'], script['output'])
        self.c.execute(statement, values)
        self.db.commit()

    def insert_current_file(self, file, file_id):
        statement = "INSERT INTO Current_file (Chat_id, File_id, Type) VALUES (?, ?, ?)"
        values = (file['chat_id'], file_id, file['type'])
        self.c.execute(statement, values)
        self.db.commit()

    def insert_filtered_file(self, file):
        statement = "INSERT INTO Filtered_Files (Original_id, Filtered_id, Filter_type)"
        values = (file['original_id'], file['filtered_id'], file['filter_type'])
        self.c.execute(statement, values)
        self.db.commit()

    def insert_files_in_chat(self, file):
        statement = "INSERT INTO Files_in_chat (Chat_id, File_id)"
        values = (file['chat_id'], file['file_id'])
        self.c.execute(statement, values)
        self.db.commit()

    def insert_filter_types(self, types):
        statement = "INSERT INTO Filter_Types (Type)"
        value = (types)
        self.c.execute(statement, value)
        self.db.commit()
    
    def delete_item(self, db_from, db_where):
        statement = "DELETE FROM {} WHERE {}".format(db_from, db_where)
        self.c.execute(statement)
        self.c.commit()