from Weather_DB import *

def run():
    test = WeatherDB()
    
    ## TESTING LIST COLUMN FUNCTION
    # print(test.get_columns('hourly_forecast'))
    # print(test.get_columns('location'))

    
    ## TESTING CREATING AND DROPPING TABLE FUNCTION
    '''
    debug = test.create_table("test1")
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
    
    # print(test.insert("location", data))
    
    ## TESTING READ FUNCTION
    for x in test.read("location"):
        print(x)
    
    
    ## TESTING GET PK
    print(test.get_pk("location"))
    
    test.close()

if __name__ == "__main__":
    run()