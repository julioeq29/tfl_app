import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium

CSS = """
h2 {
    color: deeppink;
}

.css-6qob1r {
    background: #f5cee5 !important;
}
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

px.set_mapbox_access_token(
    'pk.eyJ1Ijoiam1oYmF1ZGluNzUiLCJhIjoiY2xkYWY0aTh4MGYzaTN2bnB6NTVqcXlqeCJ9.k7_gsD6_d6aeh9EhU_0Nvw'
)

st.header('User Behaviour 💁‍♀️')

#################################################################################
########################## -- Borough data line -- ##############################
#################################################################################


@st.cache
def get_borough_data_line():
    df = pd.read_csv("data/borough_data_line.csv")
    return df


borough_line = get_borough_data_line()

b_line = px.line(
    borough_line,
    x="Year",
    y="Number_of_Bicycle_Hires",
    color='Month',
)

# b_line.update_traces(marker_line_autocolorscale="Greens")

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

bikes_daily.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))

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
    size_max=25,
    zoom=11)

station_use.update_layout(
    title_text='Most used stations',
    showlegend=True,
    width=1000,
    height=800,
    geo=dict(
        scope='europe',
        projection_type='azimuthal equal area',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
)


station_use.update_mapboxes(style="light")

st.header('Most used stations')

st.plotly_chart(station_use)


#################################################################################
######################## -- Tree Map Popular Trips -- ###########################
#################################################################################


@st.cache
def get_stations_zone():
    df = pd.read_csv("data/df_stations_zone.csv")
    return df


df_stations_zone = get_stations_zone()


def get_trips_zone(n_rows=700):
    df = pd.read_csv("data/df_trips_zones.csv", nrows=n_rows)
    return df


df_trips_zones = get_trips_zone()

df_trips_zones['lat'] = df_trips_zones.lat.apply(
    lambda x: x.strip("()").split(", "))
df_trips_zones['lon'] = df_trips_zones.lon.apply(
    lambda x: x.strip("()").split(", "))

center = {'lat': 51.509865, 'lon': -0.118092}

zones = px.scatter_mapbox(
    data_frame=df_stations_zone,
    lat='avg_lat',
    lon='avg_lon',
    center=center,
    zoom=11,
    width=1000,
    height=800,
    text=df_stations_zone.zone,
    # size_max=0.1,
)
for i in range(len(df_trips_zones)):
    zones.add_trace(
        go.Scattermapbox(lon=df_trips_zones['lon'][i],
                         lat=df_trips_zones['lat'][i],
                         mode='lines',
                         line=dict(width=2, color='red'),
                         opacity=df_trips_zones['trips_scaled'][i],
                         name=df_trips_zones['name'][i],
                         hovertext=df_trips_zones['name'][i]))

zones.update_mapboxes(style="light")

st.header('London connections')

st.write("according to a proper Londoner 🇬🇧")

st.plotly_chart(zones)

#################################################################################
######################## -- Tree Map Popular Trips -- ###########################
#################################################################################


@st.cache
def get_tree_map():
    df = pd.read_csv("data/Concentration_Of_Trips_Per_Borough.csv")
    df.index = df['boroughs']
    return df


df_tree_map = get_tree_map()
# st.write(df_tree_map)

tree_map = px.treemap(data_frame=df_tree_map,
                      path=[px.Constant("London"), df_tree_map.index],
                      values="Popular_Trips",
                      color='Popular_Trips',
                      color_continuous_scale=['lightblue', 'pink'])

tree_map.update_traces(root_color="lightgrey")

st.header('Concentration of Trips per Borough')

col1, col2, col3, col4 = st.columns(4)
col1.metric("COMBINATIONS", "604k", "88.7% realised")
col2.metric("MOST POPULAR", "Olympic", "99k")
col3.metric("2nd MOST POPULAR", "Hyde Park", "500 elec")
col4.metric("LONGEST", "17.2k", "Stratford-Putney")

st.plotly_chart(tree_map)


#################################################################################
############# -- Concentration of Stations per Borough -- #######################
#################################################################################


@st.cache
def get_concentration_stations():
    df = pd.read_csv("data/Final_Stations.csv")
    return df


df_concentration = get_concentration_stations()

concentration = px.treemap(data_frame=df_concentration,
                 path=[px.Constant("London"), 'borough'],
                 values="n_stations",
                 color='n_stations',
                 color_continuous_scale=['lightblue', 'pink'])

concentration.update_traces(root_color="lightgrey")

st.header('Concentration of Stations per Borough')

st.plotly_chart(concentration)
