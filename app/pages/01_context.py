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


col1, col2, col3 = st.columns(3)
col1.metric("MOST USED BIKE", "Id: 15,678", "5900 trips")
col2.metric("AMOUNT OF RIDES", "52M", "50% of bikes, 80% of trips")
col3.metric("BIKES IN THE SYSTEM", "12k", "500 elec")

#################################################################################
#################### -- Num of bicycle hires per year -- ########################
#################################################################################


@st.cache
def get_hires_per_year():
    df = pd.read_csv("data/month_data_streamlit.csv")
    return df


df_hires = get_hires_per_year()
fig = px.line(df_hires, x="Year", y="Number_of_Bicycle_Hires")

fig = go.Figure(fig, layout_yaxis_range=[0,12_000_000])

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

# colors = [
#     'plum', 'mediumpurple', 'palevioletred', 'pink', 'cornflowerblue',
#     'hotpink', 'darkmagenta', 'green', 'mediumvioletred', 'rebeccapurple',
#     'royalblue', 'purple'
# ]

# color_discrete_map = dict(zip(years, colors))

years = list(last_df.year_added.unique())

center = {'lat': 51.509865, 'lon': -0.118092}

fig = px.scatter_mapbox(
    data_frame=last_df,
    lat='latitude',
    lon='longitude',
    #animation_group = "exist_in_year",
    animation_frame="exist_in_year",
    # title="Evolution Of Docking stations in London",
    color='year_added',
    # color_discrete_map=color_discrete_map,
    color_continuous_scale=px.colors.sequential.Burg,
    center=center,
    zoom=11,
    size_max=20,
    width=1000,
    height=800)


fig.update_mapboxes(style="light")

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
