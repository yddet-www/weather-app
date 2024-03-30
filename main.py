from weatherDB import *

def run():
    test = weatherDB()
    print(test.list_columns('hourly_forecast'))
    print(test.get_tables())
    test.close()

if __name__ == "__main__":
    run()