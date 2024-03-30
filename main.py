from Weather_DB import *

def run():
    test = WeatherDB()
    
    ## TESTING LIST COLUMN FUNCTION
    # print(test.list_columns('hourly_forecast'))
    # print(test.list_columns('location'))
    
    ## TESTING CREATING AND DROPPING TABLE FUNCTION
    # debug = test.create_table("test1")
    # print(test.get_tables())
    # test.drop_table("test1")
    # print(test.get_tables())
    
    ## TESTING INSERT FUNCTION
    data = [('37.7749', '-122.4194', 'CA', 'San Francisco', '94105', '7th District')]
    
    print(test.insert("location", data))
    
    test.close()

if __name__ == "__main__":
    run()