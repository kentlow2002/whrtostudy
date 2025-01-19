from dotenv import load_dotenv
import os
import psycopg2
import requests
import urllib.parse
import random
from datetime import datetime, timezone

def get_all_data():
    data = []
    # Load environment variables from .env
    load_dotenv()

    # Fetch variables
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    # Connect to the database
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        #print("Connection successful!")

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Example query
        cursor.execute("SELECT * FROM places")
        result = cursor.fetchmany(10)
        #print(result)
        for row in result:
            data.append({})
            data[-1]['id'] = row[0]
            data[-1]['Name'] = row[2]
            data[-1]['FullAddress'] = row[3]
            data[-1]['CurrentUsers'] = row[4]
            data[-1]['Capacity'] = row[5]
            data[-1]['LatLng'] = str(row[6]) +', ' + str(row[7])
            data[-1]['Facilities'] = ""
            if row[8] == True:
                data[-1]['Facilities'] += "WiFi\t|\t"
            if row[9] == True:
                data[-1]['Facilities'] += "Toilets\t|\t"
            if row[10] == True:
                data[-1]['Facilities'] += "Charging ports"
            data[-1]['Images'] = []

        # Close the cursor and connection
        cursor.close()
        connection.close()
        #print("Connection closed.")

    except Exception as e:
        print(f"Failed to connect: {e}")

    return data

def push_seat(spot_name):

    data = []
    # Load environment variables from .env
    load_dotenv()

    # Fetch variables
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    # Connect to the database
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        #print("Connection successful!")

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        cursor.execute(f"SELECT seated, seats FROM places WHERE id={spot_name}")
        result = cursor.fetchone()
        newCount = 0
        if result[0] < result[1]:
            newCount = result[0]+1
            cursor.execute(f"UPDATE places SET seated={newCount} WHERE id={spot_name}")

        # Example query

        # Close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()
        #print("Connection closed.")

    except Exception as e:
        print(f"Failed to connect: {e}")

    return newCount

def pull_seat(spot_name):

    data = []
    # Load environment variables from .env
    load_dotenv()

    # Fetch variables
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    # Connect to the database
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        #print("Connection successful!")

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        cursor.execute(f"SELECT seated FROM places WHERE id={spot_name}")
        result = cursor.fetchone()

        newCount = 0
        if result[0] > 0:
            newCount = result[0]-1
            cursor.execute(f"UPDATE places SET seated={newCount} WHERE id={spot_name}")

        # Close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()
        #print("Connection closed.")

    except Exception as e:
        print(f"Failed to connect: {e}")

    return newCount
          

def push_spot(name, address, capacity, wifi, toilet, charging):
    # Load environment variables from .env
    load_dotenv()

    # Fetch variables
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    # Connect to the database
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        #print("Connection successful!")

        url = 'http://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(address) +'&format=json'
        headers = {'user-agent': 'streamlit'}
        
        geoloc = requests.get(url, headers=headers).json()

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        cursor.execute(f"SELECT MAX(id) FROM places")
        result = cursor.fetchone()
        currentDatetime = datetime.now(timezone.utc)

        cursor.execute(f"INSERT INTO places VALUES ({result[0]+1}, '{currentDatetime}', '{name}', '{address}', 0, '{capacity}', {geoloc[0]['lat']}, {geoloc[0]['lon']}, {wifi}, {toilet}, {charging});")

        # Close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()
        #print("Connection closed.")

    except Exception as e:
        print(e)

def push_email(sender, subject, msg):
    # Load environment variables from .env
    load_dotenv()

    # Fetch variables
    USER = os.getenv("user")
    PASSWORD = os.getenv("password")
    HOST = os.getenv("host")
    PORT = os.getenv("port")
    DBNAME = os.getenv("dbname")

    # Connect to the database
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME
        )
        #print("Connection successful!")

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        #cursor.execute(f"SELECT  FROM feedback")
        #result = cursor.fetchone()
        #currentDatetime = datetime.now(timezone.utc)

        cursor.execute(f"INSERT INTO feedback (sender, subject, msg) VALUES ('{sender}', '{subject}', '{msg}');")

        # Close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()
        #print("Connection closed.")

    except Exception as e:
        print(e)