from WeatherDB import *

def run():
    test = WeatherDB()
    print(test.list_columns('hourly_forecast'))
    print(test.list_columns('location'))
    print(test.get_tables())
    
    test.close()

if __name__ == "__main__":
    run()