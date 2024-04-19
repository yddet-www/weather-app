from DBConnection import *
from datetime import datetime

class DailyForecastHandler():
    
    
    def read_column_dailyForecast(self, column, limit = -1):
        enum = ["gridX", "gridY", "startTime", "title", "temp_f", "precipitate", "humidity", "windspeed", "detailedForecast"] # the only acceptable args
        
        # error check
        if not (column in enum):
            return 0
        
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = f"SELECT {column} FROM daily_forecast"
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit}"

        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_dailyForecast(self, limit = -1):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM daily_forecast "
            "ORDER BY gridX, gridY, startTime DESC "
        )
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit};"
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_pk_dailyForecast(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            "WHERE TABLE_NAME = 'daily_forecast' AND CONSTRAINT_NAME = 'PRIMARY';"
        )
        
        cursor.execute(stmt)
        
        pk = ()
        
        for key in cursor.fetchall():
            pk = pk + key
        
        connection.close()
        cursor.close()
        
        return pk
    
    
    def read_row_dailyForecast(self, gridX, gridY, startTime):
        connection = get_connection()
        cursor = connection.cursor()
        
        startTimeF = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        stmt = (
            "SELECT * FROM daily_forecast "
            f"WHERE gridX = {gridX} AND gridY = {gridY} AND startTime = '{startTimeF}'"
        )
        
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def insert_dailyForecast(self, gridX, gridY, startTime, title, temp_f, precipitate, humidity, windspeed, detailedForecast):
        stmt = (
            "INSERT INTO daily_forecast (gridX, gridY, startTime, title, temp_f, precipitate, humidity, windspeed, detailedForecast) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        
        startTimeF = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        data = (
            gridX, 
            gridY, 
            startTimeF, 
            title,
            temp_f, 
            precipitate, 
            humidity, 
            windspeed, 
            detailedForecast)
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt, data)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
    
    
    def delete_dailyForecast(self, gridX, gridY, startTime):
        startTimeF = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        stmt = f"DELETE FROM daily_forecast WHERE gridX = {gridX} AND gridY = {gridY} AND startTime = '{startTimeF}'"

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


handler = DailyForecastHandler()
# print(handler.read_column_dailyForecast("gridX"))
# print(handler.read_pk_dailyForecast())
print(handler.insert_dailyForecast(5, 30, "2024-04-18T20:00:00", "Tonight", 46, 89, 86, "5 to 10 mph", "A chance of rain showers after noon. Cloudy. High near 54, with temperatures falling to around 52 in the afternoon. Northeast wind 5 to 10 mph, with gusts as high as 20 mph. Chance of precipitation is 40%. New rainfall amounts less than a tenth of an inch possible."))
# print(handler.delete_dailyForecast(5, 30, "2024-04-18T20:00:00"))
