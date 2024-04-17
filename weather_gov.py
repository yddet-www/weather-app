import requests
import json

# Given latitude and longitude decimal values, return JSON response
def get_point(lat, lon):
    response = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
    
    if(response.status_code == 200):
        return response.json()
    
    print(f"Error retrieving API request: {response.status_code}") # print response code
    return 0 # returns 0 if API call fails

# Return state (2 characters)
def get_state(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        return response["properties"]["relativeLocation"]["properties"]["state"] # returns state
    
    return 0

# Return county (string)
def get_county(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        response = requests.get(response["properties"]["county"]).json()
        return response["properties"]["name"]
    
    return 0

# Return county ID as per NWS
def get_countyID(lat, lon):
    response = get_point(lat, lon)
    
    if(response):
        response = requests.get(response["properties"]["county"]).json()
        return response["properties"]["id"]
    
    return 0

# Return city (string)
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

# return JSON response of active alerts in the state
def get_active_alerts(lat, lon):
    params = {
        "status" : "actual",
        "area" : get_state(lat, lon),
    }
    
    response = requests.get(f"https://api.weather.gov/alerts/active", params=params).json()
    print(json.dumps(response))
    return 1