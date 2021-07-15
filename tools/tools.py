# pylint: disable=missing-docstring

import sys
import requests

BASE_URI = "https://www.metaweather.com"

def search_coordinates(lat,lon):
    target_url = BASE_URI + "/api/location/search/?lattlong="+str(round(lat,3))+','+str(round(lon,3))
    response = requests.get(target_url).json()
    print(response)
    if len(response) >= 1:
        return response[0]
    return None

def weather_forecast(woeid):
    forecast_url = "https://www.metaweather.com/api/location/"+str(woeid)
    weatherdata = requests.get(forecast_url).json()["consolidated_weather"]
    date = weatherdata[0]["applicable_date"]
    weather = weatherdata[0]["weather_state_name"]
    temp = weatherdata[0]["max_temp"]
    return date, weather, temp

def main():
    query = input("City?\n> ")
    city = search_city(query)
    if city is not None:
        weather_forecast(city["woeid"])
        return print("Are you happy? Do you want the weather for another..")
    return False

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)