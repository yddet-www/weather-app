import mysql.connector
from mysql.connector import errorcode

class weatherDB:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = "127.0.0.1", 
            user = "root", 
            password = "admin1234", 
            database = "weather-gov"
        )
        
        self.cursor = self.db.cursor()
        
    # Return a list of tables in database
    def get_tables(self):
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]
        return tables
    
    def create_table(self):
        return None
    
    def insert(self):
        return None
    
    def read(self):
        return None
    
    def update(self):   
        return None
    
    def delete(self):
        return None
    
    # ALWAYS CALL AFTER FINISHED
    def close_db(self):
        