from weatherDB import *

def run():
    test = weatherDB()
    for x in test.get_tables():
        print(x)

if __name__ == "__main__":
    run()