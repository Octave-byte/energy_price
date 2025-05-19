import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetcher import get_transfer_data, get_consumption_data
import visualizations as viz

def display_transfer_tab(data):
    """
    Display the transfer tab content
    """
    st.header("Energy Transfer Analytics")
    
    if data is None or 'transfer' not in data or data['transfer'].empty:
        st.error("No transfer data available. Please check the Airtable connection.")
        return
    
    # Get transfer and consumption data
    transfer_data = get_transfer_data(data)
    consumption_data = get_consumption_data(data) if 'consumption' in data else pd.DataFrame()
    
    if transfer_data.empty:
        st.error("No transfer data available.")
        return
    
    # Correlation matrix showing dependency between countries
    st.subheader("Energy Transfer Dependencies Between Countries")
    fig_corr = viz.plot_country_correlation_matrix(transfer_data)
    if fig_corr:
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Chart showing energy independence
    if not consumption_data.empty:
        st.subheader("Country Energy Independence")
        fig_indep = viz.plot_energy_independence(consumption_data, transfer_data)
        if fig_indep:
            st.plotly_chart(fig_indep, use_container_width=True)
    else:
        st.error("Consumption data is required to calculate energy independence.")
