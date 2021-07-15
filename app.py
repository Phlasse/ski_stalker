import streamlit as st
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium
from PIL import Image
from folium.plugins import Fullscreen
from random import randint
import json
from tools import tools
import time

st.set_page_config(layout = 'wide')

def get_latlo(address):
    geolocator = Nominatim(user_agent="busy")
    location = geolocator.geocode(address)
    loc_stats = (location.latitude, location.longitude)
    return loc_stats

Alp_center_lat = 46.2
Alp_center_lon = 9.5

img_business_lunch = Image.open("data/logos/smart_pricer.jpg")
st.image(img_business_lunch, width=300)

customer_df = pd.read_csv('data/customer.csv', sep=',')
col1, col2, col3, col4= st.beta_columns(4)
with col1:
    ###### creating the map #####
    europe_geo = r'data/europe.geojson' # geojson file
    n = folium.Map(location=[Alp_center_lat, Alp_center_lon], zoom_start=8, tiles="Stamen Terrain", width='100%')
    for index, row in customer_df[customer_df.type=='DP'].iterrows():
        pin = row.name
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country))
        folium.Marker([lat1, lon1], popup=row.name, icon=folium.Icon(color='red', icon='send'),tooltip=pin).add_to(n)
        time.sleep(1)
    for index, row in customer_df[customer_df.type=='AN'].iterrows():
        pin = row.name
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country))
        folium.Marker([lat1, lon1], popup=row.name, icon=folium.Icon(color='blue', icon='stats'),tooltip=pin).add_to(n)
        time.sleep(1)

    for index, row in customer_df[customer_df.type=='NO'].iterrows():
        pin = row.name
        print(row.customer_id)
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country))
        folium.Marker([lat1, lon1], popup=row.name, icon=folium.Icon(color='lightblue', icon='home'),tooltip=pin).add_to(n)
        time.sleep(1)
    for index, row in customer_df[customer_df.type=='LE'].iterrows():
        pin = row.name
        print(row.customer_id)
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country))
        folium.Marker([lat1, lon1], popup=row.name, icon=folium.Icon(color='lightgreen', icon='home'),tooltip=pin).add_to(n)
        time.sleep(1)  
    for index, row in customer_df[customer_df.type=='PN'].iterrows():
        pin = row.name
        print(row.customer_id)
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country))
        folium.Marker([lat1, lon1], popup=row.name, icon=folium.Icon(color='black', icon='exclamation-circle', prefix='fa'),tooltip=pin).add_to(n)
        time.sleep(1)      
    Fullscreen().add_to(n)
    style_function = lambda x: {'fillColor': '#ffffff'}# if x['features']['properties']['name']=='Austria' else '#00ff00'}
    folium.GeoJson(europe_geo, style_function=style_function).add_to(n)
    folium_static(n)
    
    
with col3:
    aletsch = Image.open("data/logos/aletsch.jpg")
    col3.image(aletsch, width=150)
with col4:
    weather_data = tools.search_coordinates(46.356,8.049)
    date, weather, temp = tools.weather_forecast(weather_data['woeid'])
    col4.write(weather+str(temp)+weather_data["title"])
st.write(customer_df)