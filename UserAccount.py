from DBConnection import *

class UserAccountHandler:

    
    # get list of datas from target column
    def read_column_userAccount(self, column, limit = -1):
        enum = ["username", "lat", "lon"]
        
        if not (column in enum):
            return 0
        
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = f"SELECT {column} FROM user_account"
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit}"
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    # return tuple of primary keys in user_account table
    def read_pk_userAccount(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            "WHERE TABLE_NAME = 'user_account' AND CONSTRAINT_NAME = 'PRIMARY';"
        )
        
        cursor.execute(stmt)
        
        pk = ()
        
        for key in cursor.fetchall():
            pk = pk + key
        
        connection.close()
        cursor.close()
        
        return pk
    
    
    # return list of rows, ordered by primary key
    def read_userAccount(self, limit = -1):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM user_account "
            "ORDER BY username "
        )
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit};"
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_row_userAccount(self, username):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM user_account "
            f"WHERE username = '{username}';"
        )
        
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def insert_userAccount(self, username, lat, lon):
        stmt = (
            "INSERT INTO user_account (username, lat, lon) "
            "VALUES (%s, %s, %s)"
        )
        
        data = (username, lat, lon)
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt, data)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
    
    
    def delete_userAccount(self, username):
        
        stmt = f"DELETE FROM user_account WHERE username = '{username}';"
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
    
    
# ###############
# TESTING AREA
# ###############

# handler = UserAccountHandler()
# print(handler.insert_userAccount("dummychang123", 41.878100, -87.629800))
# print(handler.delete_userAccount("dummychang123"))
