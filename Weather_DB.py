from DBConnection import *
from Location import LocationHandler
from WeatherAlert import WeatherAlertHandler
from LocationAlert import LocationAlertHandler
from HourlyForecast import HourlyForecastHandler
from PastForecast import PastForecastHandler
from DailyForecast import DailyForecastHandler
from UserAccount import UserAccountHandler

# ###########################################################################################
# Note to editor:
# currently, this class is expected to be used to edit all tables
# might wanna pivot into making parent classes for each table for better error handling
# as well as better functionality with specific commands for each table
# ###########################################################################################

class WeatherDB(
    LocationHandler, 
    WeatherAlertHandler, 
    LocationAlertHandler, 
    HourlyForecastHandler, 
    PastForecastHandler, 
    DailyForecastHandler, 
    UserAccountHandler):
    
    
    # Return a list of tables in database
    def get_tables(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        connection.close()
        cursor.close()
        
        return tables
    
    def alert_forecast(self):
        stmt = """
        WITH alert_locations AS (
            SELECT lat, lon, alert_id
            FROM location_alert
        )
        SELECT hf.startTime, hf.temp_f, hf.precipitate, hf.humidity, hf.wind_mph, hf.shortForecast,
            loc.state, loc.county, loc.city
        FROM hourly_forecast hf
        JOIN alert_locations al ON hf.gridX = (
            SELECT gridX FROM location WHERE lat = al.lat AND lon = al.lon
        )
        AND hf.gridY = (
            SELECT gridY FROM location WHERE lat = al.lat AND lon = al.lon
        )
        JOIN weather_alert wa ON al.alert_id = wa.alert_id
        JOIN location loc ON al.lat = loc.lat AND al.lon = loc.lon;
        """
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    def city_avg_temp(self):
        stmt = """
        SELECT l.state, l.city, AVG(df.temp_f) AS avg_temp
        FROM daily_forecast df
        JOIN location l ON df.gridX = l.gridX AND df.gridY = l.gridY
        GROUP BY l.state, l.city;
        """
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
# ###############
# TESTING AREA
# ###############