import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium
from PIL import Image
from folium.plugins import Fullscreen
from random import randint
from tools import tools


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
customer_df.set_index('name', inplace=True)
col1, col2, col3, col4= st.beta_columns(4)
with col1:
    ###### creating the map #####
    europe_geo = r'data/europe.geojson' # geojson file
    n = folium.Map(location=[Alp_center_lat, Alp_center_lon], zoom_start=6, tiles="Stamen Terrain", width='80%')
    for index, row in customer_df[customer_df.type=='DP'].iterrows():
        pin = row.name
        folium.Marker([row.lat, row.lon], popup=row.name, icon=folium.Icon(color='darkblue', icon='send'),tooltip=pin).add_to(n)
    for index, row in customer_df[customer_df.type=='AN'].iterrows():
        pin = row.name
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', '+str(row.country))
        folium.Marker([row.lat, row.lon], popup=row.name, icon=folium.Icon(color='lightblue', icon='stats'),tooltip=pin).add_to(n)
    for index, row in customer_df[customer_df.type=='NO'].iterrows():
        pin = row.name
        folium.Marker([row.lat, row.lon], popup=row.name, icon=folium.Icon(color='white', icon='home'),tooltip=pin).add_to(n)
    for index, row in customer_df[customer_df.type=='LE'].iterrows():
        pin = row.name
        folium.Marker([row.lat, row.lon], popup=row.name, icon=folium.Icon(color='lightgreen', icon='home'),tooltip=pin).add_to(n)
    for index, row in customer_df[customer_df.type=='PN'].iterrows():
        pin = row.name
        folium.Marker([row.lat, row.lon], popup=row.name, icon=folium.Icon(color='red', icon='exclamation-circle', prefix='fa'),tooltip=pin).add_to(n)
    Fullscreen().add_to(n)
    style_function = lambda x: {'fillColor': '#ffffff'}
    folium.GeoJson(europe_geo, style_function=style_function).add_to(n)
    folium_static(n)
    
    
with col3:
    distro = customer_df.groupby(by="type").count()
    distro = distro[['country']]
    distro['percent'] = distro.country / distro.country.sum() *100

    labels = distro.index
    sizes = distro.percent
    explode = (0.1, 0.1, 0, 0, 0 )
    fig1, ax1 = plt.subplots(figsize=(4,4))
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

with col4:
    col4.subheader("Market share Smart Pricer")
    country_df = pd.concat([customer_df,pd.get_dummies(customer_df['type'])], axis=1)
    country_market = country_df.groupby(by='country_abr').agg({'DP':'sum', 'AN':'sum','LE':'sum','PN':'sum','NO':'sum', 'type':'count'})
    country_market['Smart Pricer'] = 100 * (country_market.AN + country_market.DP) / country_market.type
    country_market['Price Now'] = 100 * (country_market.PN) / country_market.type

    st.write(country_market[['Smart Pricer', 'Price Now']])
    
aletsch = Image.open("data/logos/aletsch.jpg")
st.image(aletsch, width=150)
weather_data = tools.search_coordinates(46.356,8.049)
date, weather, temp = tools.weather_forecast(weather_data['woeid'])
st.write(weather+' '+str(temp)+' '+weather_data["title"])
    