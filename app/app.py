import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium

px.set_mapbox_access_token(
    'pk.eyJ1Ijoiam1oYmF1ZGluNzUiLCJhIjoiY2xkYWY0aTh4MGYzaTN2bnB6NTVqcXlqeCJ9.k7_gsD6_d6aeh9EhU_0Nvw'
)

#################################################################################
#################### -- Num of bicycle hires per year -- ########################
#################################################################################

@st.cache
def get_hires_per_year():
    df = pd.read_csv("data/month_data_streamlit.csv")
    return df


df_hires = get_hires_per_year()
fig = px.line(df_hires, x="Year", y="Number_of_Bicycle_Hires")

st.header('Number of bicycle hires per year')
st.plotly_chart(fig)

#################################################################################
#################### -- 801 bike stations in London -- ##########################
#################################################################################

@st.cache
def get_801_map():
    df = pd.read_csv("data/801_map.csv")
    return df


borough_df = get_801_map()

# Create a map focused on London, involving practical columns

practical_map = folium.Map(location=[51.509865, -0.118092],
                           zoom_start=12,
                           min_zoom=10,
                           tiles=None,
                           overlay=False)

# Create a borough marker group

borough_markers = folium.FeatureGroup(name="Borough markers",)

# For each borough, add a marker with the borough name

for lat, lng, borough in zip(borough_df['latitude'], borough_df['longitude'],borough_df['borough']):
    pop = folium.Popup(f"{borough}", parse_html=True)

    folium.CircleMarker(
        [lat, lng],
        radius=3,
        popup=pop,
        color='#e858a7',
        fill=True,
        fill_color='#e61721',
        fill_opacity=0.7,
        parse_html=False).add_to(borough_markers)

# Add the marker feature group to the map

borough_markers.add_to(practical_map)

# Add map tiles in as a toggleable feature

folium.TileLayer('OpenStreetMap', overlay=True,
                 name="Map tiles").add_to(practical_map)

# Add layer controls to the map

folium.LayerControl().add_to(practical_map)

# Display the map
st.header('Map with 801 docking stations located across central London')
folium_static(practical_map)


#################################################################################
#################### -- Num of bicycle hires per year -- ########################
#################################################################################


@st.cache
def get_borough_data_doughnut():
    df = pd.read_csv("data/borough_data_doughnut.csv")
    return df


labels_b = [
    'Westminster', 'City of London', 'Southwark', 'Tower Hamlets', 'Camden',
    'Islington', 'Hackney', 'Wandsworth', 'Kensington & Chelsea', 'Lambeth',
    'Newham', 'Hammersmith & Fulham'
]
x = borough_df['borough'].value_counts().values

borough_doughnut = get_borough_data_doughnut()

b_doughnut = go.Figure(data=[go.Pie(labels=labels_b, values=x, hole=.3)])

st.header('Breakdown per Borough')
st.plotly_chart(b_doughnut)


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
########################## -- Classic Vs E-bikes -- #############################
#################################################################################


@st.cache
def get_classic_vs_ebikes():
    df = pd.read_csv("data/classic_ebike.csv")
    return df


df_classic_vs_ebikes = get_classic_vs_ebikes()

classic_ebikes = px.bar(df_classic_vs_ebikes, x='Month', y='hires', color='bike_type')

st.header('Classic Vs eBikes')
st.plotly_chart(classic_ebikes)


#################################################################################
##################### -- Evolution of docking stations -- #######################
#################################################################################


@st.cache
def get_evolution_docking_stations():
    df = pd.read_csv("data/evolution_of_docking_stations.csv")
    return df


last_df = get_evolution_docking_stations()

colors = [
    'plum', 'mediumpurple', 'palevioletred', 'pink', 'cornflowerblue',
    'hotpink', 'darkmagenta', 'deeppink', 'mediumvioletred', 'rebeccapurple',
    'royalblue', 'purple'
]

years = list(last_df.year_added.unique())

center = {'lat': 51.509865, 'lon': -0.118092}

color_discrete_map = dict(zip(years, colors))

fig = px.scatter_mapbox(
    data_frame=last_df,
    lat='latitude',
    lon='longitude',
    #animation_group = "exist_in_year",
    animation_frame="exist_in_year",
    # title="Evolution Of Docking stations in London",
    color='year_added',
    color_discrete_map=color_discrete_map,
    center=center,
    zoom=11,
    width=1000,
    height=800)

df_flight_paths = []
for i in range(len(df_flight_paths)):
    fig.add_trace(
        go.Scattergeo(
            locationmode='USA-states',
            lon=[
                df_flight_paths['start_lon'][i], df_flight_paths['end_lon'][i]
            ],
            lat=[
                df_flight_paths['start_lat'][i], df_flight_paths['end_lat'][i]
            ],
            mode='lines',
            line=dict(width=1, color='plum'),
            opacity=float(df_flight_paths['cnt'][i]) /
            float(df_flight_paths['cnt'].max()),
        ))


st.header('Evolution Of Docking stations in London')
st.plotly_chart(fig)


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
