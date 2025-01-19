import streamlit as st
import pandas as pd
from PIL import Image
from streamlit.components.v1 import html
import settings
from db import get_all_data, push_spot

st.set_page_config(
    page_title="WhrtoStudy",
    page_icon=":books:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

settings.selected_spot_name = 0

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

data = get_all_data()

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)
st.session_state.study_spots = df.copy()
# Streamlit app
left,middle,right = st.columns(3)
if left.button(label="About",use_container_width=True):
    st.switch_page("pages/about.py")
middle.link_button(label="Github",url="https://github.com/kentlow2002/whrtostudy",use_container_width=True)
if right.button(label="Home",use_container_width=True):
    st.switch_page("home.py")
st.title("Welcome to :red[WhrtoStudy] 📚")
st.header("Find places to study in Singapore! 😎")
st.subheader("Ready to look for a study spot? 👇")
search_query = st.text_input("",placeholder="Search for a study spot", label_visibility="collapsed")
# Filter study spots based on search query
if search_query:
    filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

filtered_df.sort_values(by="Name", inplace=True)

# Display filtered study spots in the sidebar
#name_list = filtered_df["Name"].tolist()
for i in filtered_df.index:
    if st.button(label=filtered_df.loc[i]["Name"],use_container_width=True):
        settings.init()
        settings.selected_spot_name = i
        st.switch_page("pages/page.py")

st.header("Couldn't find your favourite study spot? 🤷‍♀️")
st.subheader("Let us know! 👇")

# Create a form for input
with st.form("study_spot_form"):
    # Input fields
    name = st.text_input("Name of the Study Spot", placeholder="Enter the name of the study spot")
    address = st.text_area("Address", placeholder="Enter the full address of the study spot")
    capacity = st.number_input("Capacity", min_value=1, step=1, help="Maximum number of people the spot can accommodate")

    # Checkbox for facilities
    st.write("Facilities:")
    wifi = st.checkbox("WiFi")
    toilet = st.checkbox("Toilet")
    charging_ports = st.checkbox("Charging ports")

    # File uploader for images (optional)
    images = st.file_uploader(
        "Images (Optional)", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True,
        help="Upload images of the study spot"
    )

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not name or not address:
            st.error("Please fill in the required fields: Name and Address.")
        else:
            # Collect the facilities selected
            facilities = []
            if wifi:
                facilities.append("WiFi")
            if toilet:
                facilities.append("Toilet")
            if charging_ports:
                facilities.append("Charging Ports")

            # Display the submitted data

            push_spot(name, address, capacity, wifi, toilet, charging_ports)

            st.success("Study Spot Submitted Successfully!")
            st.write("### Details of the Study Spot")
            st.write(f"**Name:** {name}")
            st.write(f"**Address:** {address}")
            st.write(f"**Capacity:** {capacity} people")
            st.write(f"**Facilities:** {', '.join(facilities) if facilities else 'None'}")

            if images:
                st.write("**Uploaded Images:**")
                for image in images:
                    st.image(image, caption=image.name, use_column_width=True)