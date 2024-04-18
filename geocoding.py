import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY") # get your own key bruh


# return dictionaries of location data from a given address (its kinda like a google search)
def search_geocode(address):
    params = {
        "q" : address,
        "api_key" : api_key
    }
    
    response = requests.get("https://geocode.maps.co/search", params=params).json()
    
    locations = []

    for location in response:
        loc_dict = {
            "display_name": location["display_name"],
            "lat": location["lat"],
            "lon": location["lon"]
        }
    
    locations.append(loc_dict)
    
    return locations


# return tuple of lat and lon from given location dictionary
def get_latlon(location):
    return (location["lat"], location["lon"])