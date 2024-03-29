import requests
from datetime import datetime
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def get_geolocation(city, country):
    api_key = 'AIzaSyB_GWE20tj8dJuPKJcENbR9TJzJyLgiILI'

    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city},{country}&key={api_key}'

    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        if latitude and longitude:
            print(f"The geographical location of {city}, {country} is Latitude: {latitude}, Longitude: {longitude}")
        else:
            print("Location not found.")
        return latitude, longitude
    else:
        return None

def get_weather(city):
    country = 'Australia'
    latitude, longitude = get_geolocation(city, country)
        # Setup the Open-Meteo API client with cache and retry on error


    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["relative_humidity_2m", "rain", "pressure_msl", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum", "wind_gusts_10m_max", "wind_direction_10m_dominant"],
        "past_days": 0,
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)
 
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_relative_humidity_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_rain = hourly.Variables(1).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(5).ValuesAsNumpy()

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()[0]
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()[0]
    daily_rain_sum = daily.Variables(2).ValuesAsNumpy()[0]
    daily_wind_gusts_10m_max = daily.Variables(3).ValuesAsNumpy()[0]
    daily_wind_direction_10m_dominant = daily.Variables(4).ValuesAsNumpy()[0]

    # Prepare data to export

    MinTemp = daily_temperature_2m_min
    MaxTemp = daily_temperature_2m_max
    Rainfall = daily_rain_sum
    WindGustDir = degrees_to_cat(daily_wind_direction_10m_dominant)
    WindGustSpeed = daily_wind_gusts_10m_max
    WindDir9am = degrees_to_cat(hourly_wind_direction_10m[9])
    WindDir3pm = degrees_to_cat(hourly_wind_direction_10m[3])
    MeanWindSpeed = (hourly_wind_speed_10m[3]+hourly_wind_speed_10m[9])/2
    MeanHumidity = (hourly_relative_humidity_2m[3]+hourly_relative_humidity_2m[9])/2
    MeanPressure = (hourly_pressure_msl[3]+hourly_pressure_msl[9])/2
    RainToday = 0
    if(Rainfall>0):
        RainToday = 1

    return MinTemp, MaxTemp, Rainfall, WindGustDir, WindGustSpeed, WindDir9am, WindDir3pm, MeanWindSpeed, MeanHumidity, MeanPressure, RainToday


def degrees_to_cat(degrees):
    # Define the cardinal directions and their corresponding degree ranges
    directions = {
        'N': (347.5, 10),
        'NNE': (10, 32.5),
        'NE': (32.5, 55),
        'ENE': (55, 77.5),
        'E': (77.5, 100),
        'ESE': (100, 122.5),
        'SE': (122.5, 145),
        'SSE': (145, 167.5),
        'S': (167.5, 190),
        'SSW': (190, 212.5),
        'SW': (212.5, 235),
        'WSW': (235, 257.5),
        'W': (257.5, 280),
        'WNW': (280, 302.5),
        'NW': (302.5, 325),
        'NNW': (325, 347.5)
    }
    cat = {'E': 0, 'ENE': 1, 'ESE': 2, 'N': 3, 'NE': 4, 'NNE': 5, 'NNW': 6, 'NW': 7, 'S': 8, 'SE': 9, 'SSE': 10, 'SSW': 11, 'SW': 12, 'W': 13, 'WNW': 14, 'WSW': 15}

    # Check if degrees fall within the defined ranges for cardinal directions
    for direction, (lower, upper) in directions.items():
        if lower <= degrees < upper:
            return cat[direction]

    # Handle the case of degrees falling between 292.5 and 337.5
    if degrees >= 347.5 or degrees < 10:
        return 3

    # If no matching direction is found, return None
    return None
