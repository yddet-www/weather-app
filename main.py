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
        self.menu = Menu(self).pack()
        
        # run
        self.mainloop()        
        
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
            
            self.pack_forget()
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
        lat = address["lat"]
        lon = address["lon"]
        
        self.master.db.insert_location(lat, 
                                       lon, 
                                       get_state(lat,lon), 
                                       get_county(lat,lon), 
                                       get_city(lat,lon), 
                                       get_countyID(lat,lon), 
                                       get_grid(lat,lon)[0], 
                                       get_grid(lat,lon)[1])
        
        self.master.db.insert_userAccount(self.usrname, lat, lon)
        self.pack_forget()
        
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