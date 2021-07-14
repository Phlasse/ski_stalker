import streamlit as st
import pandas as pd
import time
import geopy
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium
from PIL import Image
from folium.plugins import Fullscreen
from random import randint
import time
import os

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
    n = folium.Map(location=[Alp_center_lat, Alp_center_lon], zoom_start=6, tiles="Stamen Terrain", width='90%')
    for index, row in customer_df[customer_df.type=='DP'].iterrows():
        pin = row.name
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country))
        folium.Marker([lat1, lon1], popup=row.name, icon=folium.Icon(color='red', icon='send'),tooltip=pin).add_to(n)
    for index, row in customer_df[customer_df.type=='AN'].iterrows():
        pin = row.name
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country))
        folium.Marker([lat1, lon1], popup=row.name, icon=folium.Icon(color='blue', icon='stats'),tooltip=pin).add_to(n)
    Fullscreen().add_to(n)
    folium_static(n)
with col3:
    aletsch = Image.open("data/logos/aletsch.jpg")
    col3.image(aletsch, width=300)
with col4:
    col4.write("🌤 bei 22 Grad Celsius")
st.write(customer_df)


def refresher(seconds):
    while True:
        mainDir = os.path.dirname(__file__)
        filePath = os.path.join(mainDir, 'dummy.py')
        with open(filePath, 'w') as f:
            f.write(f'# {randint(0, 10000)}')
        time.sleep(seconds)
        customer_df = pd.read_csv('data/customer.csv', sep=',')

customer_df = refresher(5)