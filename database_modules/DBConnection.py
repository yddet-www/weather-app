import mysql.connector

_connection = None

def get_connection():
    global _connection
    if _connection is None:
        _connection = mysql.connector.connect(
            host = "127.0.0.1", 
            user = "root", 
            password = "admin1234", 
            database = "weather-gov",
            charset= "utf8"
        )
        
    return _connection
