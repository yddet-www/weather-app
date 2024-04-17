from Weather_DB import *
from weather_gov import *

def tes1():
    test = WeatherDB()
    
    ## TESTING LIST COLUMN FUNCTION
    # print(test.get_columns('hourly_forecast'))
    # print(test.get_columns('location'))

    ## TESTING GET PK
    # print(test.get_pk("hourly_forecast"))
    
    ## TESTING CREATING AND DROPPING TABLE FUNCTION
    '''
    test.create_table("test1")
    print(test.get_tables())
    test.drop_table("test1")
    print(test.get_tables())
    '''
    
    ## TESTING INSERT FUNCTION
    '''
    location_data = [
        ('37.7749', '-122.4194', 'CA', 'San Francisco', '94105', '7th District'),
        ('40.7128', '-74.0060', 'NY', 'New York', '10001', '9th District'),
        ('34.0522', '-118.2437', 'CA', 'Los Angeles', '90001', '12th District'),
        ('41.8781', '-87.6298', 'IL', 'Chicago', '60601', '3rd District'),
        ('29.7604', '-95.3698', 'TX', 'Houston', '77001', '18th District'),
        ('33.4484', '-112.0740', 'AZ', 'Phoenix', '85001', '5th District'),
        ('39.9526', '-75.1652', 'PA', 'Philadelphia', '19101', '1st District'),
        ('32.7767', '-96.7970', 'TX', 'Dallas', '75201', '30th District'),
        ('37.3382', '-121.8863', 'CA', 'San Jose', '95101', '15th District'),
        ('47.6062', '-122.3321', 'WA', 'Seattle', '98101', '7th District'),
        ('42.3601', '-71.0589', 'MA', 'Boston', '02101', '4th District'),
        ('25.7617', '-80.1918', 'FL', 'Miami', '33101', '27th District'),
        ('39.7392', '-104.9903', 'CO', 'Denver', '80201', '2nd District'),
        ('33.7490', '-84.3880', 'GA', 'Atlanta', '30301', '5th District'),
        ('45.5051', '-122.6750', 'OR', 'Portland', '97201', '3rd District')]
    '''
    
    # print(test.insert("location", [('10.0000', '10.0000', 'BT', 'Bumi Serpong Damai', '15321', 'Taman Jajan')]))

    ## TESTING UPDATE
    # print(test.update("location", ('10.0000', '10.0000'), ("district", "BADCDSAD")))
    
    ## TESTING DELETE
    # print(test.delete("location", ('10.0000', '10.0000')))
    
    ## TESTING READ FUNCTION
    '''
    for x in test.read("location"):
        print(x)
    '''
    
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
    # print(get_point(41.8356, -87.6308))
    print(get_state(41.8356, -87.6308))
    print(get_city(41.8356, -87.6308))
    print(get_county(41.8356, -87.6308))
    print(get_countyID(41.8356, -87.6308))

if __name__ == "__main__":
    tes2()
    # run()