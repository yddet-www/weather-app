from Weather_DB import *
from weather_gov import *
from geocoding import *
import tkinter as tk

def tes1():
    test = WeatherDB()
    
    test.close()

def run():
    main = WeatherDB()
    flag = True

    while flag:
        user = int(input(
"""
Choose option:
1) INSERT data
2) UPDATE data
3) READ data
4) DELETE data
5) EXIT
"""))
        match user:
            case 1:
                print(main.get_tables())
                table = input("Select a table name from the above existing ones:\n")
                data = []
                
                row = tuple(input(
                    "Input data following order of columns, separate by commas\n" + 
                    "Enter an empty input to end collection\n" +
                    str(main.get_columns(table)) + "\n").split(", "))
                
                while row != ('',):
                    data.append(row)
                    row = tuple(input().split(", "))
                                        
                if main.insert(table, data):
                    print("Inserting...")
                
            case 2:
                print(main.get_tables())
                table = input("Select a table name from the above existing ones:\n")
                
                conds = tuple(input(
                    "Input the target row's PK, separate by commas\n" +
                    str(main.get_pk(table)) + "\n").split(", "))
                
                data_pair = tuple(input(
                    "Input a column and its new value, separate by commas:\n" +
                    str(main.get_columns(table)) + "\n").split(", "))
                
                if main.update(table, conds, data_pair):
                    print("Updating...")

            case 3:
                print(main.get_tables())
                table = input("Select a table name from the above existing ones:\n")
                num = input("Input number of rows to print (leave empty for all):\n")
                
                if num:
                    num = int(num)
                else:
                    num = -1
                
                for x in main.read(table, num):
                    print(x)

            case 4:
                print(main.get_tables())
                table = input("Select a table name from the above existing ones:\n")
                
                target = tuple(input(
                    "Input the target row's PK, separate by commas\n" +
                    str(main.get_pk(table)) + "\n").split(", "))
                
                if main.delete(table, target):
                    print("Deleting...")

            case _:
                main.close()
                flag = False
                
def tes2():
    # print(get_alertDetails(get_StateAlertsID(39.9814515,-83.58167)[0]))
    # print(get_alertDetails("urn:oid:2.49.0.1.840.0.c72b9c45dea081f7919f4a321d01c2973796f1b4.001.1")["desc"])
    
    # print(get_zoneAlertID("OHC003"))
    # print(get_zoneAlertID("ILC031"))
  
    latlon = get_latlon(search_geocode("Cunningham Hall Bronzeville")[0])
    print(latlon)
    
    pass

if __name__ == "__main__":
    tes2()
    # run()