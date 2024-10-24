# PURPOSE: Get data from open-meteo.com and write it to a file constrained to the HSD format
# credits to open-meteo.com for the script to get the data
# and to gpt for helping me save the data in the desired format

# HOW TO INSTALL THE REQUIRED PACKAGES:
# pip install openmeteo-requests requests-cache pandas retry-requests

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

timeframe = input("Enter the desired timeframe in days before today: ")
timeframe = int(timeframe)
start_date = pd.Timestamp.today().normalize() - pd.Timedelta(days = timeframe)
end_date = pd.Timestamp.today().normalize()

start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

print("Start date:", start_date_str)
print("End date:", end_date_str)

latitude = input("Enter the latitude: ")
longitude = input("Enter the longitude: ")
print("Getting weather data...")

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": float(latitude),
	"longitude": float(longitude),
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max", "precipitation_probability_max"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch",
	"timezone": "America/Los_Angeles",
	"start_date": start_date_str,
	"end_date": end_date_str
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()
daily_wind_speed_10m_max = daily.Variables(4).ValuesAsNumpy()
daily_precipitation_probability_max = daily.Variables(5).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["weather_code"] = daily_weather_code
daily_data["temperature_max"] = daily_temperature_2m_max
daily_data["temperature_min"] = daily_temperature_2m_min
daily_data["precipitation_sum"] = daily_precipitation_sum
daily_data["wind_speed_max"] = daily_wind_speed_10m_max
daily_data["precipitation_probability_max"] = daily_precipitation_probability_max

daily_dataframe = pd.DataFrame(data = daily_data)
print(daily_dataframe)

# ... Your existing code up until creating the DataFrame ...
with open ("weatherdata.txt", "w") as file:
    for col in daily_dataframe.columns:
        if col == "date":
            file.write(f"{col}: {' '.join(daily_dataframe[col].dt.strftime('%Y-%m-%d').values)}\n")
        else:
            file.write(f"{col}: {' '.join(map(str, daily_dataframe[col].values))}\n")


    print("Data saved to weatherdata.txt")
