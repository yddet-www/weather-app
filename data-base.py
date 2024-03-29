import mysql.connector
from mysql.connector import errorcode


mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "admin1234"
)

mydb.database = "weather-gov"   # set active DB
cursor = mydb.cursor()

