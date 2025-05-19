import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetcher import get_consumption_data
import visualizations as viz

def display_consumption_tab(data):
    """
    Display the consumption tab content
    """
    st.header("Energy Consumption Analytics")
    
    if data is None or 'consumption' not in data or data['consumption'].empty:
        st.error("No consumption data available. Please check the Airtable connection.")
        return
    
    # Get consumption data for the last 30 days
    consumption_data = get_consumption_data(data, days=30)
    
    if consumption_data.empty:
        st.error("No consumption data available for the selected period.")
        return
    
    # Overall consumption of energy in Europe in the last 30d
    st.subheader("European Energy Consumption Trends (Last 30 Days)")
    fig_line = viz.plot_energy_consumption_line(consumption_data)
    if fig_line:
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Bar chart with consumption per country
    st.subheader("Energy Consumption by Country")
    fig_bar = viz.plot_country_consumption_bar(consumption_data)
    if fig_bar:
        st.plotly_chart(fig_bar, use_container_width=True)
