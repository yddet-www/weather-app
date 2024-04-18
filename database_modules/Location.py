from DBConnection import *

class LocationHandler:    
    
    
    # get list of datas from target column
    def read_column_location(self, column, limit = -1):
        enum = ["lat", "lon", "state", "county", "city", "countyID", "gridX", "gridY"] # the only acceptable args
        
        # error check
        if not (column in enum):
            return 0
        
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = f"SELECT {column} FROM location"
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit}"

        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result


    # return tuple of primary keys in location table
    def read_pk_location(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            "WHERE TABLE_NAME = 'location' AND CONSTRAINT_NAME = 'PRIMARY';"
        )
        
        cursor.execute(stmt)
        
        pk = ()
        
        for key in cursor.fetchall():
            pk = pk + key
        
        connection.close()
        cursor.close()
        
        return pk
    
    
    # return list of rows, ordered by primary key
    def read_location(self, limit = -1):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM location "
            "ORDER BY lat, lon "
        )
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit};"
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    # return a row from given lat and lon values
    def read_row_location(self, lat, lon):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM location "
            f"WHERE lat = {lat} and lon = {lon} "
        )
        
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    # insert a row into location table in database
    def insert_location(self, lat, lon, state, county, city, countyID, gridX, gridY):
        stmt = (
            "INSERT INTO location (lat, lon, state, county, city, countyID, gridX, gridY) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        
        data = (lat, lon, state, county, city, countyID, gridX, gridY)
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt, data)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
       
       
    # delete row from lat and lon values 
    def delete_location(self, lat, lon):
        
        stmt = f"DELETE FROM location WHERE lat = {lat} and lon = {lon}"
        
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

handler = LocationHandler()
print(handler.read_row_location(41.878100, -87.629800))
