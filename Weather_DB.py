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
    def get_columns(self, table):
        tuple = ()
        
        # Order by ordinal_postion basically follows the ordering as it is defined, TLDR follows the column order as seen in MySQL
        self.cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION")
        for column in self.cursor.fetchall():
            tuple = tuple + column            
        
        return tuple
    
    # Return a list of primary key(s)
    def get_pk(self, table):
        stmt = (
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            f"WHERE TABLE_NAME = '{table}' AND CONSTRAINT_NAME = 'PRIMARY'")
        
        pk = ()
        self.cursor.execute(stmt)
        
        for key in self.cursor.fetchall():
            pk = pk + key
        
        return pk
    
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
        table_columns = self.get_columns(table)
        params = ("%s",)
        
        table_tuple = ", ".join(table_columns)
        
        for _ in range(1, len(table_columns)):
            params = params + ("%s",)
            
        params = ", ".join(params)
        stmt = f"INSERT INTO {table} ({table_tuple}) VALUES ({params})"
        
        self.cursor.executemany(stmt, data) # The order of the data within the tuple matters!!!
        self.connection.commit()
        
        return 1
    
    # Returns a list of tuples from a given table
    def read(self, table, row = -1):
        stmt = f"SELECT * FROM {table}"
        result = None
        pk = ", ".join(self.get_pk(table))
        
        stmt = stmt + " ORDER BY " + pk
        
        if row != -1:
            stmt = stmt + f" LIMIT {row}"
            
        self.cursor.execute(stmt)
        result = self.cursor.fetchall()            

        return result
    
    # Update existing values of existing table
    def update(self, table, cond):
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