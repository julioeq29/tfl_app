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

st.header('Context 🚲')

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
    height=800
    )

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
######################### -- Breakdown per Borough -- ###########################
#################################################################################


@st.cache
def get_borough_data_doughnut():
    df = pd.read_csv("data/borough_data_doughnut.csv")
    return df

borough_doughnut = get_borough_data_doughnut()

labels_b = [
    'Westminster', 'City of London', 'Southwark', 'Tower Hamlets', 'Camden',
    'Islington', 'Hackney', 'Wandsworth', 'Kensington & Chelsea', 'Lambeth',
    'Newham', 'Hammersmith & Fulham'
]
x = borough_doughnut['borough'].value_counts().values


b_doughnut = go.Figure(data=[go.Pie(labels=labels_b, values=x, hole=.3)])

st.header('Breakdown per Borough')
st.plotly_chart(b_doughnut)
