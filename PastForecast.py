from DBConnection import *
from datetime import datetime 
    
class PastForecastHandler:

    def read_column_pastForecast(self, column, limit = -1):
        enum = ["gridX", "gridY", "startTime", "temp_f", "precipitate", "humidity", "wind_mph", "shortForecast"] # the only acceptable args
        
        # error check
        if not (column in enum):
            return 0
        
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = f"SELECT {column} FROM past_forecast"
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit}"

        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_pastForecast(self, limit = -1):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM past_forecast "
            "ORDER BY gridX, gridY, startTime DESC "
        )
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit};"
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_pk_pastForecast(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            "WHERE TABLE_NAME = 'past_forecast' AND CONSTRAINT_NAME = 'PRIMARY';"
        )
        
        cursor.execute(stmt)
        
        pk = ()
        
        for key in cursor.fetchall():
            pk = pk + key
        
        connection.close()
        cursor.close()
        
        return pk
    
    
    def read_row_pastForecast(self, gridX, gridY, startTime):
        connection = get_connection()
        cursor = connection.cursor()
        
        startTimeF = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        stmt = (
            "SELECT * FROM past_forecast "
            f"WHERE gridX = {gridX} AND gridY = {gridY} AND startTime = '{startTimeF}'"
        )
        
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def insert_pastForecast(self, gridX, gridY, startTime, temp_f, precipitate, humidity, wind_mph, shortForecast):
        stmt = (
            "INSERT INTO past_forecast (gridX, gridY, startTime, temp_f, precipitate, humidity, wind_mph, shortForecast) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        )
        
        startTimeF = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        data = (
            gridX, 
            gridY, 
            startTimeF, 
            temp_f, 
            precipitate, 
            humidity, 
            wind_mph, 
            shortForecast)
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt, data)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
    
    
    def delete_pastForecast(self, gridX, gridY, startTime):
        startTimeF = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        stmt = f"DELETE FROM past_forecast WHERE gridX = {gridX} AND gridY = {gridY} AND startTime = '{startTimeF}'"

        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1