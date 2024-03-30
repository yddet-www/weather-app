import mysql.connector
from datetime import date, datetime, time
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
        
        # Order by ordinal_postion basically follows the ordering as it is defined, TLDR follows the column order as seen in MySQL
        self.cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION")
        for column in self.cursor.fetchall():
            tuple = tuple + column            
        
        return tuple
    
    # For the sake of the video
    def create_table(self, table):
        dummy_table = (
            f"CREATE TABLE `{table}` ("
            "`row_no` int(11) NOT NULL,"
            "`birth_date` date NOT NULL,"
            "`first_name` varchar(14) NOT NULL,"
            "`last_name` varchar(16) NOT NULL,"
            "`gender` enum('M','F') NOT NULL,"
            "`graduation_date` date NOT NULL,"
            "PRIMARY KEY (`row_no`))"
        )
        
        self.cursor.execute(dummy_table)
        return 1
    
    # For the sake of cleaning up the mess for the video
    def drop_table(self, table):
        self.cursor.execute(f"DROP TABLE {table}")
        return 1
    
    # Insert data(s) into target table
    def insert(self, table, data):
        table_columns = self.list_columns(table)
        params = ("%s",)
        
        table_tuple = ", ".join(table_columns)
        
        for _ in range(1, len(table_columns)):
            params = params + ("%s",)
            
        params = ", ".join(params)
        stmt = f"INSERT INTO {table} ({table_tuple}) VALUES ({params})"
        
        self.cursor.executemany(stmt, data) # The order of the data within the tuple matters!!!
        self.connection.commit()
        
        return 1
        
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