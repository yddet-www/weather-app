import requests
import json

# given latitude and longitude decimal values, return JSON response
def get_point(lat, lon):
    response = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
    
    if(response.status_code == 200):
        return response.json()
    
    print(f"Error retrieving API request: {response.status_code}") # print response code
    return 0 # returns 0 if API call fails


# return tuple of grid location as per NWS (x, y)
def get_grid(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        return (response["properties"]["gridX"], response["properties"]["gridY"])
    
    return 0
    

# return state (2 characters)
def get_state(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        return response["properties"]["relativeLocation"]["properties"]["state"] # returns state
    
    return 0


# return county (string)
def get_county(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        response = requests.get(response["properties"]["county"]).json()
        return response["properties"]["name"]
    
    return 0


# return county ID as per NWS
def get_countyID(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        response = requests.get(response["properties"]["county"]).json()
        return response["properties"]["id"]
    
    return 0


# return city (string)
def get_city(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        return response["properties"]["relativeLocation"]["properties"]["city"] # returns city
    
    return 0


# return JSON response of daily forecast API request
def get_dailyForecast(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        response = requests.get(response["properties"]["forecast"]).json()
        return response
    
    return 0


# return JSON response of hourly forecast API request
def get_hourlyForecast(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        response = requests.get(response["properties"]["forecastHourly"]).json()
        return response
    
    return 0


# return list of active alert IDs in a state
def get_StateAlertsID(state):
    params = {
        "status" : "actual",
        "area" : state,
    }
    
    response = requests.get(f"https://api.weather.gov/alerts/active", params=params).json()
    weather_alerts = [i["properties"]["id"] for i in response["features"]]
        
    return weather_alerts # note that value may return NULL if no alerts active


# return list  of alert IDs in a zone/county ID
def get_zoneAlertID(zone):
    params = {
        "status" : "actual",
        "zone" : zone
    }
    
    response = requests.get(f"https://api.weather.gov/alerts/active", params=params).json()
    weather_alerts = [i["properties"]["id"] for i in response["features"]]
    
    return weather_alerts


# returns dictionary of weather details from given alert ID
def get_alertDetails(alert_id):
    response = requests.get(f"https://api.weather.gov/alerts/{alert_id}").json()
    
    data = {
        "event" : response["properties"]["event"],
        "onset" : response["properties"]["onset"],
        "ends" : response["properties"]["ends"],
        "desc" : response["properties"]["description"],
        "instruction" : response["properties"]["instruction"],
    }
    
    return data