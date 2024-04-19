from DBConnection import *


###################################################
# Note:
# I intentionally left out the delete function 
# because the database does it for us when
# an alert is deleted
###################################################


class LocationAlertHandler:
    
    
    def read_column_locationAlert(self, column, limit = -1):
        enum = ["lat", "lon", "alert_id"] # the only acceptable args
        
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
    
    
    def insert_locationAlert(self, lat, lon, alert_id):
        stmt = (
            "INSERT INTO location_alert (lat, lon, alert_id) "
            "VALUES (%s, %s, %s)"
        )
        
        data = (lat, lon, alert_id)
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt, data)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
    
    
# ###############
# TESTING AREA
# ###############


# handler = LocationAlertHandler()
# print(handler.insert_locationAlert(41.878100, -87.629800,"urn:oid:2.49.0.1.840.0.c72b9c45dea081f7919f4a321d01c2973796f1b4.001.1"))
# print(handler.read_rowByID_locationAlert("urn:oid:2.49.0.1.840.0.c72b9c45dea081f7919f4a321d01c2973796f1b4.001.1"))
# print(handler.read_rowByLatLon_locationAlert(41.878100, -87.629800))
# print(handler.read_locationAlert())
# print(handler.read_pk_locationAlert())
# print(handler.read_column_locationAlert("alert_id"))