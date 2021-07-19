# pylint: disable=missing-docstring
import requests
import pandas as pd
from geopy.geocoders import Nominatim


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

def get_latlo(address):
    geolocator = Nominatim(user_agent="busy")
    location = geolocator.geocode(address)
    loc_stats = (location.latitude, location.longitude)
    return loc_stats

def add_latlon_df(df):
    for index, row in df.iterrows():
        if row.lat != None:   
            try:
                query = row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country)
                lat, lon = get_latlo(query)
                df.loc[df.index==index,'lat'] = lat    
                df.loc[df.index==index,'lon'] = lon    
            except:
                try:
                    lat, lon = get_latlo(row.address)
                    df.loc[df.index==index,'lat'] = lat
                    df.loc[df.index==index,'lon'] = lon
                except:
                    print(row.address, ' could not be found')
    df.to_csv('../data/customer1.csv', index=False)
            
if __name__ == '__main__':
    add_latlon_df(pd.read_csv('../data/customer1.csv'))