import streamlit as st
import pandas as pd
from PIL import Image
from streamlit.components.v1 import html
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

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

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT * FROM places")
    result = cursor.fetchmany(5)
    print(result)
    for row in result:
        data.append({})
        data[-1]['Name'] = row[2]
        data[-1]['FullAddress'] = row[3]
        data[-1]['CurrentUsers'] = row[4]
        data[-1]['Capacity'] = row[5]
        data[-1]['LatLng'] = str(row[6]) +', ' + str(row[7])
        data[-1]['Facilities'] = ""
        if row[8] == True:
            data[-1]['Facilities'] += "WiFi"
        if row[9] == True:
            data[-1]['Facilities'] += "Toilets"
        if row[10] == True:
            data[-1]['Facilities'] += "Charging ports"


    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Streamlit app
st.title("Study Spots in Singapore")

# Sidebar for navigation and search
st.title("Navigation")
search_query = st.text_input("Search for a study spot")

# Filter study spots based on search query
if search_query:
    filtered_df = df[df["Name"].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# Display filtered study spots in the sidebar
name_list = filtered_df["Name"].tolist()
for i in range(len(name_list)):
    button = st.button(f"{name_list[i]}",key=i)
    if button:
        selected_spot_name = name_list[i]
        break

#Use Session State to manage user count
if "study_spots" not in st.session_state:
    st.session_state.study_spots = df.copy()
if "counter" not in st.session_state:
    st.session_state.counter = True

st.switch_page(f"pages/page.py")