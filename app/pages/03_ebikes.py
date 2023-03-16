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

st.header('eBikes 🏍')

#################################################################################
########################## -- Classic Vs E-bikes -- #############################
#################################################################################


@st.cache
def get_classic_vs_ebikes():
    df = pd.read_csv("data/classic_vs_ebike-2.csv")
    return df


df_classic_vs_ebikes = get_classic_vs_ebikes()

x = df_classic_vs_ebikes['Month']
y = df_classic_vs_ebikes['% Ebike Bikes']
y2 = df_classic_vs_ebikes['% Classic Bikes']

classic_ebikes = go.Figure()
classic_ebikes.add_bar(x=x, y=y)
classic_ebikes.add_bar(x=x, y=y2)
classic_ebikes.update_layout(barmode="relative",
                  xaxis={'categoryorder': 'category ascending'})

st.header('Classic Vs eBikes')

col1, col2, col3 = st.columns(3)
col1.metric("OCTOBER", "5.5%")
col2.metric("NOVEMBER", "6.6%", "+1.1%")
col3.metric("DECEMBER", "7.3%", "+0.7%")

st.plotly_chart(classic_ebikes)
