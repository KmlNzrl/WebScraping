import streamlit as st
import requests
import pandas as pd

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="McDonald's Outlets Viewer", layout="wide")
st.title("McDonald's Outlet In Kuala Lumpur")

# Navigation
options = st.sidebar.selectbox("Choose a search method...",[
    "View all outlets",
    "Search by outlets ID",
    "Search by outlets name",
    "View outlets with geolocation"
])

if options == "View all outlets":
    st.header("All Outlets In Kuala Lumpur")
    # Fetch all outlets from API
    response = requests.get(f"{API_BASE_URL}/outlets")
    if response.status_code == 200:
        data = response.json()["data"]
        df = pd.DataFrame(data).sort_values("id").reset_index(drop=True)
        st.dataframe(df)
        
    else:
        st.error("Failed to retrieve outlets")

elif options == "Search by outlets ID":
    st.header("Search by Outlets ID")
    outlet_id = st.number_input("Enter Outlet ID....", min_value=1, step=1)
    if st.button("Search"):
        response = requests.get(f"{API_BASE_URL}/outlets/search/id", params={"outlets_id":outlet_id})
        if response.status_code == 200:
            st.json(response.json()["data"])
        else:
            st.error("Failed to retrieve outlet")

elif options == "Search by outlets name":
    st.header("Search by Outlets Name")
    outlet_name = st.text_input("Enter Outlet Name....")
    if st.button("Search"):
        response = requests.get(f"{API_BASE_URL}/outlets/search/name", params={"name":outlet_name})
        if response.status_code == 200:
            df = pd.DataFrame(response.json()["data"]).sort_values(by="id").reset_index(drop=True)
            st.dataframe(df)
        else:
            st.error("Failed to retrieve outlet")

elif options == "View outlets with geolocation":
    st.header("Outlets with Geolocation")
    response = requests.get(f"{API_BASE_URL}/outlets/with-geolocation")
    if response.status_code == 200:
        data = response.json()["data"]
        df = pd.DataFrame(data).sort_values(by="id").reset_index(drop=True)
        # st.dataframe(df)
        st.map(df[['latitude', 'longitude']].rename(columns={'latitude': 'lat', 'longitude': 'lon'}))
    else:
        st.error("Failed to retrieve geolocation data.")