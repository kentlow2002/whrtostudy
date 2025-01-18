import streamlit as st
import pandas as pd
from PIL import Image
from streamlit.components.v1 import html
import home
from home import *

#Use Session State to manage user count
if "study_spots" not in st.session_state:
    st.session_state.study_spots = df.copy()
if "counter" not in st.session_state:
    st.session_state.counter = True

# Function to display the study spot details
def display_study_spot(spot):
    counter = True
    st.subheader(spot["Name"])
    st.write(f"**Capacity:** {spot['Capacity']} people")
    st.write(f"**Current Users:** {spot['CurrentUsers']} people")
    st.write(f"**Facilities:** {spot['Facilities']}")
    st.write(f"**Address:** {spot['FullAddress']}")

    # Map showing the location of the study spot with a marker
    lat, lon = map(float, spot["LatLng"].split(", "))
    map_data = pd.DataFrame({"lat": [lat], "lon": [lon]})
    st.map(map_data, zoom=15, use_container_width=True)

    st.write("**Images:**")
    if spot["Images"]:
        carousel_html = """
        <div style='display: flex; overflow-x: auto; gap: 10px;'>
        """
        for image_url in spot["Images"]:
            carousel_html += f"<div style='min-width: 300px;'><img src='{image_url}' alt='Image' style='width: 100%; border: 1px solid #ddd; border-radius: 4px;'></div>"
        carousel_html += "</div>"
        html(carousel_html, height=300)

    # Interactive buttons for user presence
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"I am here! ({spot['Name']})"):
            # Update the number of current users
            index = st.session_state.study_spots[
                st.session_state.study_spots["Name"] == spot["Name"]
            ].index[0]
            if st.session_state.counter:
                st.session_state.study_spots.at[index, "CurrentUsers"] += 1
                st.session_state.counter = False
                st.error(f"Successfully Updated!")
            else:
                st.error("Please stop spamming!")
    with col2:
        if st.button(f"I'm leaving ({spot['Name']})"):
            index = st.session_state.study_spots[
                st.session_state.study_spots["Name"] == spot["Name"]
            ].index[0]
            if st.session_state.study_spots.at[index, "CurrentUsers"] > 0:
                if not st.session_state.counter:
                    st.session_state.study_spots.at[index, "CurrentUsers"] -= 1
                    st.session_state.counter = True
                    st.error("Sucessfully Updated!")
                else:
                    st.error("How can you leave a place you never entered?")
            else:
                st.error(f"{spot['Name']} is empty!")

# Find the selected study spot and display its details
selected_spot = st.session_state.study_spots[
    st.session_state.study_spots["Name"] == selected_spot_name
].iloc[0]
display_study_spot(selected_spot)