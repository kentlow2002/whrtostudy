import streamlit as st
import pandas as pd
from PIL import Image
from streamlit.components.v1 import html
#from home import *
import settings
from db import push_seat, pull_seat, get_all_data

st.set_page_config(
    page_title="Studying here?",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "study_spots" not in st.session_state:
    st.switch_page('home.py')
if "counter" not in st.session_state:
    st.session_state.counter = True

# Function to display the study spot details
def display_study_spot(spot):
    counter = True
    st.subheader(spot["Name"])
    st.write(f"**Capacity:** {spot['Capacity']} people")
    currentUsers = st.empty()
    currentUsers.write(f"**Current Users:** {spot['CurrentUsers']} people")
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
            carousel_html += f"""<div style='min-width: 300px; height: 200px; overflow: hidden; display: flex; align-items: center; justify-content: center;'>
            <img src='{image_url}' alt='Image' style='width: auto; height: 100%; border: 1px solid #ddd; border-radius: 4px; object-fit: cover;'>
        </div>"""
        carousel_html += "</div>"
        html(carousel_html, height=300)

    # Interactive buttons for user presence
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"I am here @ {spot['Name']}!"):
            # Update the number of current users
            index = st.session_state.study_spots[
                st.session_state.study_spots["Name"] == spot["Name"]
            ].index[0]
            if st.session_state.counter and settings.commit:
                st.session_state.study_spots.at[index, "CurrentUsers"] += 1
                currentUsers.write(f"**Current Users:** {push_seat(spot_name=spot['id'])} people")
                st.session_state.counter = False
                settings.commit = 0
                st.error(f"Successfully Updated!")
            else:
                st.error("Please stop spamming!")
    with col2:
        if st.button(f"I'm leaving {spot['Name']}"):
            index = st.session_state.study_spots[
                st.session_state.study_spots["Name"] == spot["Name"]
            ].index[0]
            if st.session_state.study_spots.at[index, "CurrentUsers"] > 0:
                if not st.session_state.counter and not settings.commit:
                    st.session_state.study_spots.at[index, "CurrentUsers"] -= 1
                    currentUsers.write(f"**Current Users:** {pull_seat(spot_name=spot['id'])} people")
                    st.session_state.counter = True
                    settings.commit = 1
                    st.error("Sucessfully Updated!")
                else:
                    st.error("How can you leave a place you never entered?")
            else:
                st.error(f"{spot['Name']} is empty!")

# Find the selected study spot and display its details
#print(st.session_state.study_spots.iloc[settings.selected_spot_name])
print(settings.selected_spot_name)
selected_spot = st.session_state.study_spots.loc[settings.selected_spot_name]
left,middle,right = st.columns(3)
if left.button(label="About",use_container_width=True):
    st.switch_page("pages/about.py")
middle.link_button(label="Github",url="https://github.com/kentlow2002/whrtostudy",use_container_width=True)
if right.button(label="Home",use_container_width=True):
    st.switch_page("home.py")
display_study_spot(selected_spot)