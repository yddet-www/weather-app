from DBConnection import *

class LocationAlertHandler:
    
    
    def read_column_locationAlert(self, column, limit = -1):
        enum = ["alert_id", "lat", "lon"] # the only acceptable args
        
        # error check
        if not (column in enum):
            return 0
        
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = f"SELECT {column} FROM location_alert"
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit}"

        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_pk_locationAlert(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            "WHERE TABLE_NAME = 'location_alert' AND CONSTRAINT_NAME = 'PRIMARY';"
        )
        
        cursor.execute(stmt)
        
        pk = ()
        
        for key in cursor.fetchall():
            pk = pk + key
        
        connection.close()
        cursor.close()
        
        return pk
    
    
    def read_locationAlert(self, limit = -1):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM location_alert "
            "ORDER BY alert_id "
        )
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit};"
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_rowByID_locationAlert(self, alert_id):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM location_alert "
            f"WHERE alert_id = '{alert_id}' "
        )
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_rowByLatLon_locationAlert(self, lat, lon):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM location_alert "
            f"WHERE lat = {lat} AND lon = {lon} "
        )
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result