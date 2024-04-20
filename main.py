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
        
        self.text1 = ttk.Label(self, text="Insert Username")
        self.text1.pack(expand=True, fill="both")
        
        self.input_field = ttk.Entry(self)
        self.input_field.pack()
                    
        self.submit = ttk.Button(self, text="Submit", command=self.get_usrname)
        self.submit.pack()
        
    def get_usrname(self):
        usrname = self.input_field.get()
        
        if self.master.db.read_row_userAccount(usrname):
            self.text1["text"] = usrname
        else:
            self.text1["text"] = "Username not found! Creating account..."
        
def run():
    WeatherApp()


if __name__ == "__main__":
    run()
    # tes2()
    # run_console()