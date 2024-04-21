from Weather_DB import *
from weather_gov import *
from geocoding import *
import tkinter as tk
from tkinter import ttk

class WeatherApp(tk.Tk):
    def __init__(self):
        # Main page setup
        super().__init__()
        
        self.db = WeatherDB()
        self.lat = None
        self.lon = None
        
        self.title("Weather App")
        self.geometry("960x540")
        self.minsize(960,540)
        
        # widgets
        self.menu = Menu(self)
        self.action = Action(self)
        self.option = Option(self)
        self.forecast = Forecast(self)
        self.alert = Alert(self)
        
        # start it off
        self.menu.pack()
        
        # run
        self.mainloop()
        
class Forecast(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_mainWidgets()
        
    def create_mainWidgets(self):
        self.text1 = ttk.Label(self, text="THIS IS FORECAST WINDOW")
        self.text1.pack(expand=True, fill="both")
        
        self.back = ttk.Button(self, text="Change location", command=lambda : (self.pack_forget(), self.master.option.pack()))
        self.back.pack(expand=True, fill="both")
        
class Alert(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_mainWidgets()
        
    def create_mainWidgets(self):
        self.text1 = ttk.Label(self, text="THIS IS ALERT WINDOW")
        self.text1.pack(expand=True, fill="both")
        
        self.back = ttk.Button(self, text="Change location", command=lambda : (self.pack_forget(), self.master.option.pack()))
        self.back.pack(expand=True, fill="both")
        
class Option(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_mainWidgets()
        
    def create_mainWidgets(self):
        self.text1 = ttk.Label(self, text="THIS IS OPTION WINDOW")
        self.text1.pack(expand=True, fill="both")
        
        self.back = ttk.Button(self, text="Change location", command=lambda : (self.pack_forget(), self.master.action.pack()))
        self.back.pack(expand=True, fill="both")
        
        self.forecast = ttk.Button(self, text="Get forecast", command=lambda : (self.pack_forget(), self.master.forecast.pack()))
        self.forecast.pack(expand=True, fill="both")
 
        self.alert = ttk.Button(self, text="Check for alerts", command=lambda : (self.pack_forget(), self.master.alert.pack()))
        self.alert.pack(expand=True, fill="both")
        
class Action(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_mainWidgets()
        
    def create_mainWidgets(self):
        self.text1 = ttk.Label(self, text="Choose an option")
        self.text1.pack(expand=True, fill="both")
        
        self.user_address = ttk.Button(self, text="Use account address", command=self.user_next)
        self.user_address.pack(expand=True, fill="both")
        
        self.other_address = ttk.Button(self, text="Use different address", command=self.other_next)
        self.other_address.pack(expand=True, fill="both")
        
    def user_next(self):   
        self.pack_forget()
        self.master.option.pack()

        
    def other_next(self):
        self.user_address.pack_forget()
        self.other_address.pack_forget()
        
        self.text1["text"] = "Search an address"
        
        self.address_buttons = []
        
        self.input = ttk.Entry(self)
        self.input.pack(ipadx=50)
        
        self.submit = ttk.Button(self, text="Submit", command=self.get_address)
        self.submit.pack()
        
    def get_address(self):
        self.address = self.input.get()
        
        result = search_geocode(self.address)
        
        self.clear_addressWidgets()
        
        if result:      # error check if API call found anything
            for i in result:
                if get_point(i["lat"], i["lon"]) != 0:
                    self.create_addressWidgets(i)   # if search result is within bounds, create button 
        else:
            self.text1["text"] = "No address found, use different keywords"
            
    def create_addressWidgets(self, address):
        button = ttk.Button(self, text=address["display_name"], command=lambda addr=address: self.set_address(addr))
        button.pack()
        self.address_buttons.append(button)
        
    def clear_addressWidgets(self):
        # Remove all existing buttons
        for button in self.address_buttons:
            button.destroy()
            
        self.address_buttons = []
        
    def set_address(self, address):
        lat = round(float(address["lat"]), 6)
        lon = round(float(address["lon"]), 6)
        
        check = self.master.db.read_row_location(lat, lon)
                
        if not check:
            self.master.db.insert_location(lat, 
                                            lon, 
                                            get_state(lat,lon), 
                                            get_county(lat,lon), 
                                            get_city(lat,lon), 
                                            get_countyID(lat,lon), 
                                            get_grid(lat,lon)[0], 
                                            get_grid(lat,lon)[1])
                
        self.master.lat = lat
        self.master.lon = lon
        
        self.pack_forget()
        self.master.forecast.pack()
                
class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_mainWidgets()
        
        self.address_buttons = []
        
    def create_mainWidgets(self):
        self.text1 = ttk.Label(self, text="Insert Username")
        self.text1.pack(expand=True, fill="both")
        
        self.text2 = ttk.Label(self)
        self.text2.pack(expand=True, fill="both")
        
        self.input_field = ttk.Entry(self)
        self.input_field.pack(ipadx=50)
                    
        self.submit = ttk.Button(self, text="Submit", command=self.get_usrname)
        self.submit.pack()
        
    def get_usrname(self):
        self.usrname = self.input_field.get()
        
        if self.usrname == "":
            self.text1["text"] = "Don't leave it blank! Insert another username"
        
        # If username is in the database, set lat and lon values for session
        elif self.master.db.read_row_userAccount(self.usrname):
            self.text1["text"] = self.usrname
            
            acc = self.master.db.read_row_userAccount(self.usrname)[0]
            
            self.master.lat = acc[1]
            self.master.lon = acc[2]
            
            self.pack_forget()
            self.master.action.pack()
        else:
            self.text1["text"] = "Username not found! Creating account..."
            self.text2["text"] = "Bind account to an address"
            self.submit["command"] = self.get_address
            
    def get_address(self):
        self.address = self.input_field.get()
        self.text2["text"] = "Bind account to an address"
        
        result = search_geocode(self.address)
        
        self.clear_addressWidgets()
        
        if result:      # error check if API call found anything
            for i in result:
                if get_point(i["lat"], i["lon"]) != 0:
                    self.create_addressWidgets(i)   # if search result is within bounds, create button 
        else:
            self.text2["text"] = "No address found, use different keywords"
            
    def create_addressWidgets(self, address):
        button = ttk.Button(self, text=address["display_name"], command=lambda addr=address: self.set_address(addr))
        button.pack()
        self.address_buttons.append(button)
        
    def set_address(self, address):
        lat = round(float(address["lat"]), 6)
        lon = round(float(address["lon"]), 6)
        
        check = self.master.db.read_row_location(lat, lon)
                
        if not check:
            self.master.db.insert_location(lat, 
                                            lon, 
                                            get_state(lat,lon), 
                                            get_county(lat,lon), 
                                            get_city(lat,lon), 
                                            get_countyID(lat,lon), 
                                            get_grid(lat,lon)[0], 
                                            get_grid(lat,lon)[1])
        
        self.master.db.insert_userAccount(self.usrname, lat, lon)
        
        self.master.lat = lat
        self.master.lon = lon
        
        self.pack_forget()
        self.master.action.pack()
        
    def clear_addressWidgets(self):
        # Remove all existing buttons
        for button in self.address_buttons:
            button.destroy()
            
        self.address_buttons = []  # Clear the list of button references
        
def run():
    WeatherApp()


if __name__ == "__main__":
    run()
    # tes2()
    # run_console()