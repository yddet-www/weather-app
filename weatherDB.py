import mysql.connector
from mysql.connector import errorcode

class WeatherDB:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = "127.0.0.1", 
            user = "root", 
            password = "admin1234", 
            database = "weather-gov",
            charset= "utf8"
        )
        
        self.cursor = self.connection.cursor()
    
    # Return a list of tables in database
    def get_tables(self):
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]
        return tables
    
    # Returns a tuple of a table's columns
    def list_columns(self, table):
        tuple = ()
        
        self.cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
        for column in self.cursor.fetchall():
            tuple = tuple + column            
        
        return tuple
    
    # For the sake of the video
    def create_table(self, table, tuple):
        return None
    
    # Insert tuple onto target table
    def insert(self, table, tuple):
        return None
    
    # Thinking of creating seperate read functions for each table, but idk
    def read(self):
        return None
    
    # Update existing values of existing table
    def update(self):   
        return None
    
    # Delete tuple from existing table
    def delete(self):
        return None
    
    # ALWAYS CALL AFTER FINISHED
    def close(self):
        if self.cursor:
            print("Closing cursor...")
            self.cursor.close()
        
        if self.connection:
            print("Closing connection...")
            self.connection.close()