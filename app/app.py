import streamlit as st
from PIL import Image


CSS = """

body {
  text-align: center;
}

h2 {
    color: deeppink;
    font-size: 6.25rem;
}

span {
    color: deeppink;
}

.css-6qob1r {
    background: #f5cee5 !important;
}

.css-1v0mbdj {
  # max-width: 200px;
}

.main {
  background-image: url("https://images.unsplash.com/photo-1524435823394-99adce70ee08?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1960&q=80.png");
}
"""

st.markdown(f'<style>{CSS}</style>', unsafe_allow_html=True)


st.header('TFL BIKES')

st.subheader('System Analysis')

# image = Image.open("tfl-logo.png")
# bikes = Image.open("bikes.png")

# st.image(bikes)
# st.image(image)











#################################################################################
#################### -- 801 bike stations in London -- ##########################
#################################################################################


# @st.cache
# def get_801_map():
#     df = pd.read_csv("data/801_map.csv")
#     return df


# borough_df = get_801_map()

# # Create a map focused on London, involving practical columns

# practical_map = folium.Map(location=[51.509865, -0.118092],
#                            zoom_start=12,
#                            min_zoom=10,
#                            tiles=None,
#                            overlay=False)

# # Create a borough marker group

# borough_markers = folium.FeatureGroup(name="Borough markers", )

# # For each borough, add a marker with the borough name

# for lat, lng, borough in zip(borough_df['latitude'], borough_df['longitude'],
#                              borough_df['borough']):
#     pop = folium.Popup(f"{borough}", parse_html=True)

#     folium.CircleMarker([lat, lng],
#                         radius=3,
#                         popup=pop,
#                         color='#e858a7',
#                         fill=True,
#                         fill_color='#e61721',
#                         fill_opacity=0.7,
#                         parse_html=False).add_to(borough_markers)

# # Add the marker feature group to the map

# borough_markers.add_to(practical_map)

# # Add map tiles in as a toggleable feature

# folium.TileLayer('OpenStreetMap', overlay=True,
#                  name="Map tiles").add_to(practical_map)

# # Add layer controls to the map

# folium.LayerControl().add_to(practical_map)

# # Display the map
# st.header('Map with 801 docking stations located across central London')
# folium_static(practical_map)
