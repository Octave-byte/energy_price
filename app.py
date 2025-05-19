import streamlit as st
import time
from apscheduler.schedulers.background import BackgroundScheduler
from tabs import price, production, consumption, transfer
from data_fetcher import fetch_all_data, get_cached_data

# Page configuration
st.set_page_config(
    page_title="European Energy Analytics Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for data caching
if 'data' not in st.session_state:
    st.session_state.data = None
    st.session_state.last_updated = None

# Function to update data
def update_data():
    try:
        st.session_state.data = fetch_all_data()
        st.session_state.last_updated = time.time()
        print("Data updated at:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.session_state.last_updated)))
    except Exception as e:
        print(f"Error updating data: {e}")

# Create a background scheduler to update data hourly
scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', hours=1)
scheduler.start()

# Initialize data on first load
if st.session_state.data is None:
    with st.spinner("Loading initial data..."):
        update_data()

# Main app
st.title("European Energy Analytics Dashboard")

# Last updated info
if st.session_state.last_updated:
    st.caption(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.session_state.last_updated))}")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Price", "Production", "Consumption", "Transfer"])

# Get cached data
data = get_cached_data(st.session_state.data)

# Display tabs content
with tab1:
    price.display_price_tab(data)
    
with tab2:
    production.display_production_tab(data)
    
with tab3:
    consumption.display_consumption_tab(data)
    
with tab4:
    transfer.display_transfer_tab(data)

# Cleanup when app stops
def on_shutdown():
    scheduler.shutdown()

import atexit
atexit.register(on_shutdown)
