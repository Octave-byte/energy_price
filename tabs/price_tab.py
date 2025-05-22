import streamlit as st
from utils.helpers import (
    compute_avg_price_by_country,
    compute_price_volatility_by_country,
    compute_price_percentile_by_country,
    compute_weighted_avg_price_europe
)

def render(price_df, load_df):

    st.subheader("Europe-wide Weighted Average Price (in €/MWH)")
    europe_df = compute_weighted_avg_price_europe(price_df, load_df)
    europe_dict = dict(zip(europe_df['period'], europe_df['weighted_avg_price']))

    col1, col2 = st.columns(2)
    col1.metric("Average Price (1 Day)", f"{europe_dict.get('1d', 0):,.1f} €/MWh")
    col2.metric("Average Price (7 Days)", f"{europe_dict.get('7d', 0):,.1f} €/MWh")

    st.divider()

    st.subheader("Average Electricity Prices in €/MWH")
    df_avg = compute_avg_price_by_country(price_df).rename(columns={
        'country_name': 'Country',
        'avg_1d': 'Avg. 1 Day',
        'avg_7d': 'Avg. 7 Days',
        'avg_30d': 'Avg. 30 Days'
    })
    st.dataframe(df_avg, use_container_width=True)

    st.divider()

    st.subheader("Price Volatility (Standard Deviation)")
    df_vol = compute_price_volatility_by_country(price_df).rename(columns={
        'country_name': 'Country',
        'std_1d': 'Std. Dev 1 Day',
        'std_7d': 'Std. Dev 7 Days',
        'std_30d': 'Std. Dev 30 Days'
    })
    st.dataframe(df_vol, use_container_width=True)

    st.divider()

    st.subheader("Price Percentile Ranking")
    df_pct = compute_price_percentile_by_country(price_df).rename(columns={
        'country_name': 'Country',
        'avg_price': 'Average Price',
        'price_percentile': 'Percentile Rank'
    })
    st.dataframe(df_pct, use_container_width=True)

    
