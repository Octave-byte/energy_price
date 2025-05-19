import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetcher import get_production_data
import visualizations as viz

def display_production_tab(data):
    """
    Display the production tab content
    """
    st.header("Energy Production Analytics")
    
    if data is None or 'production' not in data or data['production'].empty:
        st.error("No production data available. Please check the Airtable connection.")
        return
    
    # Get production data for the last 30 days
    production_data = get_production_data(data, days=30)
    
    if production_data.empty:
        st.error("No production data available for the selected period.")
        return
    
    # Overall production of energy in Europe in the last 30d (with evolution of mix)
    st.subheader("European Energy Production Mix (Last 30 Days)")
    fig_area = viz.plot_energy_production_line(production_data)
    if fig_area:
        st.plotly_chart(fig_area, use_container_width=True)
    
    # Create two columns for the next visualizations
    col1, col2 = st.columns(2)
    
    # Table with energy mix for each country
    with col1:
        st.subheader("Energy Mix by Country")
        mix_table = viz.create_energy_mix_table(production_data)
        if mix_table is not None:
            st.dataframe(mix_table, use_container_width=True)
    
    # Bar chart with energy mix for each country
    with col2:
        st.subheader("Energy Mix Visualization")
        fig_mix = viz.plot_energy_mix_bar(production_data)
        if fig_mix:
            st.plotly_chart(fig_mix, use_container_width=True)
