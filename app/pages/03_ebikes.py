import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
import folium

px.set_mapbox_access_token(
    'pk.eyJ1Ijoiam1oYmF1ZGluNzUiLCJhIjoiY2xkYWY0aTh4MGYzaTN2bnB6NTVqcXlqeCJ9.k7_gsD6_d6aeh9EhU_0Nvw'
)

st.header('eBikes 🏍')

#################################################################################
########################## -- Classic Vs E-bikes -- #############################
#################################################################################


@st.cache
def get_classic_vs_ebikes():
    df = pd.read_csv("data/classic_ebike.csv")
    return df


df_classic_vs_ebikes = get_classic_vs_ebikes()

classic_ebikes = px.bar(df_classic_vs_ebikes,
                        x='Month',
                        y='hires',
                        color='bike_type')

st.header('Classic Vs eBikes')
st.plotly_chart(classic_ebikes)
