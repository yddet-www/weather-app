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

class WeatherDB(LocationHandler, ):
    
    
    # Return a list of tables in database
    def get_tables(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        connection.close()
        cursor.close()
        
        return tables
    
    
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
            
            
# ###############
# TESTING AREA
# ###############

db = WeatherDB()
print(db.get_tables())