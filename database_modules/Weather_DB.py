from DBConnection import *
from datetime import date, datetime, time
from mysql.connector import errorcode

# ###########################################################################################
# Note to editor:
# currently, this class is expected to be used to edit all tables
# might wanna pivot into making parent classes for each table for better error handling
# as well as better functionality with specific commands for each table
# ###########################################################################################

class WeatherDB:
    def __init__(self):
        self.connection = get_connection()
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
    # Condition limited to PK comparison, and data_pair is expecting a tuple pair
    def update(self, table, pk_cond, data_pair):
        stmt = f"UPDATE {table} SET {data_pair[0]} = '{data_pair[1]}' "
        pk = self.get_pk(table)
        cond = f"WHERE {pk[0]} = '{pk_cond[0]}'"
        
        for i in range(1, len(pk)):
            cond = cond + f" AND {pk[i]} = '{pk_cond[i]}'"
        
        stmt = stmt + cond
        self.cursor.execute(stmt)
        
        return 1
    
    # Delete tuple from existing table
    def delete(self, table, pk_cond):
        pk = self.get_pk(table)
        cond = f"WHERE {pk[0]} = '{pk_cond[0]}'"
       
        for i in range(1, len(pk)):
            cond += f" AND {pk[i]} = '{pk_cond[i]}'"
       
        stmt = f"DELETE FROM {table} {cond}"
        self.cursor.execute(stmt)
        self.connection.commit()
       
        return 1
    
    # ALWAYS CALL AFTER FINISHED
    def close(self):
        if self.cursor:
            print("Closing cursor...")
            self.cursor.close()
        
        if self.connection:
            print("Closing connection...")
            self.connection.close()
            