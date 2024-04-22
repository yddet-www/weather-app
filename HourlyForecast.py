from DBConnection import *
from datetime import datetime

class HourlyForecastHandler():
    
    
    def read_column_hourlyForecast(self, column, limit = -1):
        enum = ["gridX", "gridY", "startTime", "temp_f", "precipitate", "humidity", "wind_mph", "shortForecast"] # the only acceptable args
        
        # error check
        if not (column in enum):
            return 0
        
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = f"SELECT {column} FROM hourly_forecast"
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit}"

        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_hourlyForecast(self, limit = -1):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM hourly_forecast "
            "ORDER BY gridX, gridY, startTime DESC "
        )
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit};"
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_pk_hourlyForecast(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            "WHERE TABLE_NAME = 'hourly_forecast' AND CONSTRAINT_NAME = 'PRIMARY';"
        )
        
        cursor.execute(stmt)
        
        pk = ()
        
        for key in cursor.fetchall():
            pk = pk + key
        
        connection.close()
        cursor.close()
        
        return pk
    
    
    def read_row_hourlyForecast(self, gridX, gridY, startTime):
        connection = get_connection()
        cursor = connection.cursor()
        
        startTimeF = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        stmt = (
            "SELECT * FROM hourly_forecast "
            f"WHERE gridX = {gridX} AND gridY = {gridY} AND startTime = '{startTimeF}'"
        )
        
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def insert_hourlyForecast(self, gridX, gridY, startTime, temp_f, precipitate, humidity, wind_mph, shortForecast):
        stmt = (
            "INSERT INTO hourly_forecast (gridX, gridY, startTime, temp_f, precipitate, humidity, wind_mph, shortForecast) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            "ON DUPLICATE KEY UPDATE "
            "temp_f = VALUES(temp_f), "
            "precipitate = VALUES(precipitate), "
            "humidity = VALUES(humidity), "
            "wind_mph = VALUES(wind_mph), "
            "shortForecast = VALUES(shortForecast);"
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
    
    
    def log_hourlyForecast(self):
        stmt2 = (
            "INSERT INTO past_forecast "
            "SELECT * "
            "FROM hourly_forecast "
            "WHERE startTime < DATE_SUB(NOW(), INTERVAL 1 HOUR); "
        )
        
        stmt1 = (
            "DELETE FROM hourly_forecast "
            "WHERE startTime < DATE_SUB(NOW(), INTERVAL 1 HOUR); "
        )
    
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt2)
        connection.commit()
        
        cursor.execute(stmt1)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
    
    
    def delete_hourlyForecast(self, gridX, gridY, startTime):
        startTimeF = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        stmt = f"DELETE FROM hourly_forecast WHERE gridX = {gridX} AND gridY = {gridY} AND startTime = '{startTimeF}'"

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


# handler = HourlyForecastHandler()
# print(handler.read_column_hourlyForecast("gridX"))
# print(handler.read_pk_hourlyForecast())
# print(handler.insert_hourlyForecast(5, 30, "2024-04-18T20:00:00", 46, 89, 86, 15, "Rain Showers"))
# print(handler.delete_hourlyForecast(5, 30, "2024-04-18T20:00:00"))
