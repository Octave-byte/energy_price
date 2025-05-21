import streamlit as st
from utils.helpers import (
    compute_avg_price_by_country,
    compute_price_volatility_by_country,
    compute_price_percentile_by_country,
    compute_weighted_avg_price_europe
)

def render(price_df, load_df):
    st.subheader("Average Electricity Prices")
    st.dataframe(compute_avg_price_by_country(price_df), use_container_width=True)

    st.subheader("Price Volatility (Standard Deviation)")
    st.dataframe(compute_price_volatility_by_country(price_df), use_container_width=True)

    st.subheader("Price Percentile Ranking")
    st.dataframe(compute_price_percentile_by_country(price_df), use_container_width=True)

    st.subheader("Europe-wide Weighted Average Price")
    st.dataframe(compute_weighted_avg_price_europe(price_df, load_df), use_container_width=True)
