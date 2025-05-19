import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetcher import get_price_data
import visualizations as viz

def display_price_tab(data):
    """
    Display the price tab content
    """
    st.header("Energy Price Analytics")
    
    if data is None or 'price' not in data or data['price'].empty:
        st.error("No price data available. Please check the Airtable connection.")
        return
    
    # Get price data for the last 30 days
    price_data = get_price_data(data, days=30)
    
    if price_data.empty:
        st.error("No price data available for the selected period.")
        return
    
    # Overall price energy in Europe in the last 30d
    st.subheader("European Energy Price Trends (Last 30 Days)")
    fig_line = viz.plot_energy_price_line(price_data)
    if fig_line:
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Create two columns for the next visualizations
    col1, col2 = st.columns(2)
    
    # Bar chart with current price for each country in Europe
    with col1:
        st.subheader("Current Energy Prices by Country")
        fig_bar = viz.plot_country_price_bar(price_data)
        if fig_bar:
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Table with price today, 7d ago, 30d ago for each country
    with col2:
        st.subheader("Price Comparison Over Time")
        comparison_table = viz.create_price_comparison_table(price_data)
        if comparison_table is not None:
            st.dataframe(comparison_table, use_container_width=True)
