from DBConnection import *
from datetime import datetime

class WeatherAlertHandler():    
    
    
    # get list of datas from target column
    def read_column_weatherAlert(self, column, limit = -1):
        enum = ["alert_id", "title", "onset", "ending", "descript", "instruction"] # the only acceptable args
        
        # error check
        if not (column in enum):
            return 0
        
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = f"SELECT {column} FROM weather_alert"
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit}"

        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    # ngerti lah, gausah gw jelasin
    def read_pk_weatherAlert(self):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            "WHERE TABLE_NAME = 'weather_alert' AND CONSTRAINT_NAME = 'PRIMARY';"
        )
        
        cursor.execute(stmt)
        
        pk = ()
        
        for key in cursor.fetchall():
            pk = pk + key
        
        connection.close()
        cursor.close()
        
        return pk
    
    
    def read_weatherAlert(self, limit = -1):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM weather_alert "
            "ORDER BY alert_id "
        )
        
        if (limit != -1):
            stmt = stmt + f" LIMIT {limit};"
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    def read_row_weatherAlert(self, alert_id):
        connection = get_connection()
        cursor = connection.cursor()
        
        stmt = (
            "SELECT * FROM weather_alert "
            f"WHERE lat = '{alert_id}' "
        )
            
        cursor.execute(stmt)
        result = cursor.fetchall()
        
        connection.close()
        cursor.close()
        
        return result
    
    
    # assuming dates are as passed from NWS in the format %Y-%m-%dT%H:%M:%S (removed timezone, datetime is local time)
    def insert_weatherAlert(self, alert_id, title, onset, ending, descript, instruction):
        stmt = (
            "INSERT INTO weather_alert (alert_id, title, onset, ending, descript, instruction)"
            "VALUES (%s, %s, %s, %s, %s, %s)"
            "ON DUPLICATE KEY UPDATE "
                "title = VALUES(title), "
                "onset = VALUES(onset), "
                "ending = VALUES(ending), "
                "descript = VALUES(descript), "
                "instruction = VALUES(instruction); "
        )
        
        onsetF = datetime.strptime(onset, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        endingF = datetime.strptime(ending, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        data = (
            alert_id, 
            title, 
            onsetF, 
            endingF, 
            descript, 
            instruction)
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt, data)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
    
    
    def refresh_weatherAlert(self):
        stmt = f"DELETE FROM weather_alert WHERE ending < NOW()"
        
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(stmt)
        connection.commit()
        
        connection.close()
        cursor.close()
        
        return 1
    
    
    def delete_weatherAlert(self, alert_id):
        
        stmt = f"DELETE FROM weather_alert WHERE alert_id = '{alert_id}'"
        
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


# sample_alert = ("urn:oid:2.49.0.1.840.0.c72b9c45dea081f7919f4a321d01c2973796f1b4.001.1", 
#                 "Severe Thunderstorm Warning", 
#                 "2024-04-17T13:59:00", 
#                 "2024-04-17T14:30:00", 
#                 "At 158 PM EDT, severe thunderstorms were located along a line\nextending from 6 miles east of Paulding to near Continental to near\nDelphos to near Spencerville In Allen County, moving east at 35 mph.\n\nHAZARD...60 mph wind gusts and quarter size hail.\n\nSOURCE...Radar indicated.\n\nIMPACT...Hail damage to vehicles is expected. Expect wind damage to\nroofs, siding, and trees.\n\nLocations impacted include...\nLima, Delphos, Ottawa, Spencerville, Columbus Grove, Leipsic, Elida,\nKalida, Continental, Holgate, Glandorf, Ottoville, Spencerville In\nAllen County, Middle Point, Cairo, Fort Jennings, Grover Hill,\nDupont, Melrose, and Florida.", 
#                 "A Tornado Watch remains in effect until 700 PM EDT for northwestern\nand west central Ohio.\n\nRemain alert for a possible tornado! Tornadoes can develop quickly\nfrom severe thunderstorms. If you spot a tornado go at once into the\nbasement or small central room in a sturdy structure.\n\nFor your protection move to an interior room on the lowest floor of a\nbuilding.\n\nTorrential rainfall is occurring with these storms, and may lead to\nflash flooding. Do not drive your vehicle through flooded roadways.")

# handler = WeatherAlertHandler()
# print(handler.read_pk_weatherAlert())
# print(handler.read_column_weatherAlert("descript")[0][0])
# print(handler.insert_weatherAlert(
#     sample_alert[0], 
#     sample_alert[1], 
#     sample_alert[2], 
#     sample_alert[3], 
#     sample_alert[4], 
#     sample_alert[5]))
# print(handler.delete_weatherAlert("urn:oid:2.49.0.1.840.0.c72b9c45dea081f7919f4a321d01c2973796f1b4.001.1"))