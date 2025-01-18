import streamlit as st
import pandas as pd
from PIL import Image
from streamlit.components.v1 import html
import settings
from db import get_all_data

# Hardcoded database of study spots
data = [
    {
        "Name": "Tampines Hub Level 5",
        "Capacity": 20,
        "Images": [
            "https://thesmartlocal.com/wp-content/uploads/2019/07/study-spots-15.png",
            "https://cdn.shopify.com/s/files/1/0273/3935/8281/files/Our_Tampines_Hub_2_600x600.png?v=1623744796",
            "https://workingwithgrace.wordpress.com/wp-content/uploads/2017/11/our-tampines-hub-study-corner.jpg?w=584&h=389"
        ],
        "Facilities": "Toilet nearby, Charging spot, Wifi",
        "LatLng": "1.3528, 103.9396",  # Latitude and Longitude
        "FullAddress": "1 Tampines Walk, Singapore 528523",
        "CurrentUsers": 0
    },
    {
        "Name": "Study Spot B",
        "Capacity": 30,
        "Images": ["https://example.com/image_b1.jpg", "https://example.com/image_b2.jpg", "https://example.com/image_b3.jpg"],
        "Facilities": "Toilet nearby, Wifi",
        "LatLng": "1.3000, 103.8000",
        "FullAddress": "456 Secondary Road, Singapore 654321",
        "CurrentUsers": 0
    },
    {
        "Name": "Study Spot C",
        "Capacity": 100,
        "Images": ["https://example.com/image_c1.jpg"],
        "Facilities": "Charging spot, Wifi",
        "LatLng": "1.2800, 103.8500",
        "FullAddress": "789 Tertiary Avenue, Singapore 987654",
        "CurrentUsers": 0
    }
]

data = data + get_all_data()

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)
# Streamlit app
st.title("Study Spots in Singapore")

# Sidebar for navigation and search
st.title("Welcome to :red[WhrtoStudy] 📚")
st.header("Find places to study in Singapore! 😎")
st.subheader("Ready to look for a study spot? 👇")
search_query = st.text_input("",placeholder="Search for a study spot", label_visibility="collapsed")
# Filter study spots based on search query
if search_query:
    filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# Display filtered study spots in the sidebar
name_list = filtered_df["Name"].tolist()
for i in range(len(name_list)):
    check = st.checkbox(label=name_list[i],value=0,key=i)
    if check:
        settings.init()
        settings.selected_spot_name = name_list[i]
        st.switch_page("pages/page.py")
