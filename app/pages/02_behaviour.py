import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium

px.set_mapbox_access_token(
    'pk.eyJ1Ijoiam1oYmF1ZGluNzUiLCJhIjoiY2xkYWY0aTh4MGYzaTN2bnB6NTVqcXlqeCJ9.k7_gsD6_d6aeh9EhU_0Nvw'
)

st.header('Behaviour 🚀')

#################################################################################
########################## -- Borough data line -- ##############################
#################################################################################


@st.cache
def get_borough_data_line():
    df = pd.read_csv("data/borough_data_line.csv")
    return df


borough_line = get_borough_data_line()

b_line = px.line(borough_line,
                 x="Year",
                 y="Number_of_Bicycle_Hires",
                 color='Month')

st.header('Monthly number of bicycle hires')
st.plotly_chart(b_line)



#################################################################################
####################### -- Count of hires pattern -- ############################
#################################################################################


@st.cache
def get_count_of_hires_pattern():
    df = pd.read_csv("data/count_of_hires_pattern.csv")
    return df


df_everyday = get_count_of_hires_pattern()

bikes_daily = px.line(df_everyday,
                      x="hour_slots",
                      y="count_of_bike_hires",
                      color='week_day')

st.header('Daily bike hires pattern')
st.plotly_chart(bikes_daily)


#################################################################################
########################### -- Most used stations -- ############################
#################################################################################


@st.cache
def get_stations_used():
    df = pd.read_csv("data/df_station_use_scaled.csv")
    return df


df_station_use = get_stations_used()

station_use = px.scatter_mapbox(
    df_station_use,
    lat="Station_latitude",
    lon="Station_longitude",
    hover_name='All_trips_starting_ending_here',
    size=df_station_use['scaled_trip_total'],
    color="All_trips_starting_ending_here",
    color_continuous_scale=px.colors.sequential.Burg,
    size_max=15,
    zoom=11)

station_use.update_layout(
    title_text='Most used stations',
    showlegend=True,
    geo=dict(
        scope='europe',
        projection_type='azimuthal equal area',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)

st.header('Most used stations')
st.plotly_chart(station_use)



#################################################################################
######################## -- Tree Map Popular Trips -- ###########################
#################################################################################


@st.cache
def get_tree_map():
    df = pd.read_csv("data/Concentration_Of_Trips_Per_Borough.csv")
    return df


df_tree_map = get_tree_map()

tree_map = px.treemap(data_frame=df_tree_map,
                      path=[px.Constant("London"), df_tree_map.index],
                      values="Popular_Trips",
                      color='Popular_Trips',
                      color_continuous_scale=['lightblue', 'pink'])

tree_map.update_traces(root_color="lightgrey")

st.header('Most popular trips')
st.plotly_chart(tree_map)
