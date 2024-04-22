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
        self.forecast = None
        self.alert = None
        
        # start it off
        self.menu.pack()
        
        # run
        self.mainloop()
        
class Alert(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_mainWidgets()
        
        self.alertWidgets = []
        
    def create_mainWidgets(self):
        self.text1 = ttk.Label(self, text="Select an alert option")
        self.text1.pack(expand=True, fill="both")
        
        self.back = ttk.Button(self, text="Back", command=lambda : (self.pack_forget(), self.master.option.pack()))
        self.back.pack(expand=True, fill="both")
        
        self.alert = ttk.Button(self, text="Check active alerts", command=self.weather_alerts)
        self.alert.pack(expand=True, fill="both")
        
    def weather_alerts(self):
        active_alert = get_pointAlertID(self.master.lat, self.master.lon)
        
        self.clear_alertWidgets()
        
        if active_alert:
            for i in active_alert:
                alert_id = i
                detail = get_alertDetails(i)
                
                title = detail["event"]
                onset = detail["onset"][:-6]
                ending = detail["ends"][:-6]
                descript = detail["desc"]
                instruction = detail["instruction"]
                
                self.master.db.refresh_weatherAlert()
                self.master.db.insert_weatherAlert(alert_id, title, onset, ending, descript, instruction)
                self.master.db.insert_locationAlert(self.master.lat, self.master.lon, alert_id)
                
                alerting = (
                    f"{title}\n"
                    f"onset: {onset}\n"
                    f"end: {ending}\n"
                    f"\n{descript}\n"
                    f"\n{instruction}\n"
                )
                
                label = ttk.Label(self, text=alerting, background='#FFFFCC', padding=4)
                label.pack(side=tk.LEFT, expand=True, fill="both", padx=4, pady=16)
                
                self.alertWidgets.append(label)
        else:
            label = ttk.Label(self, text="No alerts found, rest easy", background='#FFFFCC', padding=4)
            label.pack(side=tk.LEFT, expand=True, fill="both", padx=4, pady=16)
            self.alertWidgets.append(label)
    
    def clear_alertWidgets(self):
        # Remove all existing widgets
        for widget in self.alertWidgets:
            widget.destroy()
            
        self.alertWidgets = []  # Clear the list of label references
        
class Forecast(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.gridXY = get_grid(self.master.lat, self.master.lon)
        self.create_mainWidgets()
        
        self.forecastWidgets = []
        
    def create_mainWidgets(self):
        curr_loc = self.master.db.read_row_location(self.master.lat, self.master.lon)[0]
        state = curr_loc[2]
        county = curr_loc[3]
        city = curr_loc[4]
        
        self.text1 = ttk.Label(self, text=f"Current location: {city}, {county} County {state}")
        self.text1.pack(expand=True, fill="both")
        
        self.back = ttk.Button(self, text="Back", command=lambda : (self.pack_forget(), self.master.option.pack()))
        self.back.pack(expand=True, fill="both")
        
        self.hourly = ttk.Button(self, text="Get hourly forecast", command=self.hourly_forecast)
        self.hourly.pack(expand=True, fill="both")
        
        self.daily = ttk.Button(self, text="Get daily forecast", command=self.daily_forecast)
        self.daily.pack(expand=True, fill="both")
        
        self.past = ttk.Button(self, text="Get past forecast", command= self.past_forecast)
        self.past.pack(expand=True, fill="both")
        
        self.weather_alert_forecast = ttk.Button(self, text="Check forecast of \nalerted areas", command= self.alert_forecast)
        self.weather_alert_forecast.pack(expand=True, fill="both")
        
        self.city_temp = ttk.Button(self, text="Check average temperature \nof registered cities", command= self.avg_cityTemp)
        self.city_temp.pack(expand=True, fill="both")
        
        
    def avg_cityTemp(self):
        self.text1["text"] = "Fetching alerted area forecast..."
        self.hourly["text"] = "Get hourly forecast"
        self.daily["text"] = "Get daily forecast"
        self.past["text"] = "Get past forecast"
        self.weather_alert_forecast["text"] = "Check forecast of \nalerted areas"
        self.city_temp["text"] = "Refresh"
        
        avg = self.master.db.city_avg_temp()
        
        self.clear_forecastWidgets()
        
        for i in avg:
            text = (
                f"{i[1]}, {i[0]} average temperature: {i[2]}"
            )
            
            label = ttk.Label(self, text=text, background='#FFFFCC', padding=4)
            label.pack(expand=True, fill="both", pady=4)
            
            self.forecastWidgets.append(label)
            
        
    def alert_forecast(self):
        self.text1["text"] = "Fetching alerted area forecast..."
        self.hourly["text"] = "Get hourly forecast"
        self.daily["text"] = "Get daily forecast"
        self.past["text"] = "Get past forecast"
        self.weather_alert_forecast["text"] = "Refresh"
        self.city_temp["text"] = "Check average temperature \nof registered cities"
        
        alert = self.master.db.alert_forecast()
        
        self.clear_forecastWidgets()
        
        for i in alert:
            startTime = i[0]
            temp_f = i[1]
            precipitate = i[2]
            humidity = i[3]
            wind_mph = i[4]
            shortForecast = i[5]
            state = i[6]
            county = i[7]
            city = i[8]
            
            
            forecasting = (
                f"{startTime}\n"
                f"temperature: {temp_f} F\n"
                f"precipitate: {precipitate}\n"
                f"humidity: {humidity}\n"
                f"wind: {wind_mph}\n"
                f"{shortForecast}\n"
                f"{city} {county}, {state}"
            )
            
            label = ttk.Label(self, text=forecasting, background='#FFFFCC', padding=4, wraplength=120)
            label.pack(side=tk.LEFT, expand=True, fill="both", padx=4, pady=16)
            
            self.forecastWidgets.append(label)
    
    def hourly_forecast(self):
        self.text1["text"] = "Fetching hourly forecast..."
        self.hourly["text"] = "Refresh"
        self.daily["text"] = "Get daily forecast"
        self.past["text"] = "Get past forecast"
        self.weather_alert_forecast["text"] = "Check forecast of \nalerted areas"
        self.city_temp["text"] = "Check average temperature \nof registered cities"
        
        hourly = get_hourlyForecast(self.master.lat, self.master.lon)["properties"]["periods"]
        
        self.clear_forecastWidgets()
        self.master.db.log_hourlyForecast()
                
        for i in range(12):
            period = hourly[i]
            
            startTime = period["startTime"][:-6]
            temp_f = period["temperature"]
            precipitate = period["probabilityOfPrecipitation"]["value"]
            humidity = period["relativeHumidity"]["value"]
            wind_mph = int(period["windSpeed"].split()[0])
            shortForecast = period["shortForecast"]
            
            self.master.db.insert_hourlyForecast(self.gridXY[0], 
                                                 self.gridXY[1], 
                                                 startTime, 
                                                 temp_f, 
                                                 precipitate, 
                                                 humidity, 
                                                 wind_mph, 
                                                 shortForecast)
            
            forecasting = (
                f"{startTime[5:7]}/{startTime[8:10]}, {startTime[11:]}\n"
                f"temperature: {temp_f} F\n"
                f"precipitation: {precipitate}%\n"
                f"humidty: {humidity}%\n"
                f"wind: {wind_mph} mph\n"
                f"{shortForecast}\n"
            )
            
            label = ttk.Label(self, text=forecasting, background='#FFFFCC', padding=4, width=16)
            label.pack(side=tk.LEFT, expand=True, fill="both", padx=4, pady=16)
            
            self.forecastWidgets.append(label)
            
    def clear_forecastWidgets(self):
        # Remove all existing buttons
        for label in self.forecastWidgets:
            label.destroy()
            
        self.forecastWidgets = []  # Clear the list of label references
            
    def daily_forecast(self):
        self.text1["text"] = "Fetching daily forecast..."
        self.hourly["text"] = "Get hourly forecast"
        self.daily["text"] = "Refresh"
        self.past["text"] = "Get past forecast"
        self.weather_alert_forecast["text"] = "Check forecast of \nalerted areas"
        self.city_temp["text"] = "Check average temperature \nof registered cities"
        
        daily = get_dailyForecast(self.master.lat, self.master.lon)["properties"]["periods"]
               
        self.clear_forecastWidgets()
        self.master.db.refresh_dailyForecast()
        
        for i in range(12):
            period = daily[i]
            
            startTime = period["endTime"][:-6]
            title = period["name"]
            temp_f = period["temperature"]
            precipitate = period["probabilityOfPrecipitation"]["value"]
            
            if not precipitate:
                precipitate = 0
            
            humidity = period["relativeHumidity"]["value"]
            windspeed = period["windSpeed"]
            detailedForecast = period["detailedForecast"]
            
            self.master.db.insert_dailyForecast(self.gridXY[0], 
                                                self.gridXY[1],
                                                startTime,
                                                title,
                                                temp_f,
                                                precipitate,
                                                humidity,
                                                windspeed,
                                                detailedForecast)
            
            forecasting = (
                f"{title}\n"
                f"temperature: {temp_f} F\n"
                f"precipitation: {precipitate}%\n"
                f"humidty: {humidity}%\n"
                f"wind: {windspeed}\n"
                f"\n{detailedForecast}\n"
            )
            
            label = ttk.Label(self, text=forecasting, background='#FFFFCC', padding=4, width=20, wraplength=120)
            label.pack(side=tk.LEFT, expand=True, fill="both", padx=4, pady=16)
            
            self.forecastWidgets.append(label)
    
    def past_forecast(self):
        self.text1["text"] = "Fetching past forecast..."
        self.hourly["text"] = "Get hourly forecast"
        self.daily["text"] = "Get daily forecast"
        self.past["text"] = "Refresh"
        self.weather_alert_forecast["text"] = "Check forecast of \nalerted areas"
        self.city_temp["text"] = "Check average temperature \nof registered cities"
        
        past = self.master.db.read_row_pastForecast(self.gridXY[0], self.gridXY[1])
        
        self.clear_forecastWidgets()
        
        if len(past) > 12:
            limit = 12
        else:
            limit = len(past)

        for i in range(limit):
            period = past[i]
            
            date = period[2].strftime("%Y-%m-%d %H:%M:%S")
            temp = period[3]
            precipitate = period[4]
            humidity = period[5]
            wind = period[6]
            shortForecast = period[7]
            
            forecasting = (
                f"{date}\n"
                f"temperature: {temp} F\n"
                f"precipitation: {precipitate}%\n"
                f"humidty: {humidity}%\n"
                f"wind: {wind} mph\n"
                f"{shortForecast}\n"
            )
            
            label = ttk.Label(self, text=forecasting, background='#FFFFCC', padding=4, width=18)
            label.pack(side=tk.LEFT, expand=True, fill="both", padx=4, pady=16)
            
            self.forecastWidgets.append(label)
        
class Option(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_mainWidgets()
        
    def create_mainWidgets(self):
        self.text1 = ttk.Label(self, text="Choose the following options")
        self.text1.pack(expand=True, fill="both")
        
        self.back = ttk.Button(self, text="Change location", command=lambda : (self.pack_forget(), self.master.action.pack()))
        self.back.pack(expand=True, fill="both")
        
        self.forecast = ttk.Button(self, text="Get forecast", command=self.move_forecast)
        self.forecast.pack(expand=True, fill="both")
 
        self.alert = ttk.Button(self, text="Check for alerts", command=self.move_alert)
        self.alert.pack(expand=True, fill="both")
        
    def move_forecast(self):
        self.master.forecast = Forecast(self.master)
        self.master.forecast.pack()
        self.pack_forget()
        
    def move_alert(self):
        self.master.alert = Alert(self.master)
        self.master.alert.pack()
        self.pack_forget()
        
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
        self.master.forecast = Option(self.master)
        self.master.forecast.pack()
                
class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_mainWidgets()
        
        self.address_buttons = []
        
    def create_mainWidgets(self):
        self.text1 = ttk.Label(self, text="Insert username")
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