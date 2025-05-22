import streamlit as st
from utils.helpers import (
    compute_daily_total_load_30d,
    compute_total_load_by_country
)

def render(load_df):
    st.subheader("Daily Total Load (Last 30 Days)")
    daily = compute_daily_total_load_30d(load_df)
    latest = daily.sort_values('day', ascending=False).iloc[0]

    col1, col2 = st.columns(2)
    col1.metric("Total Load (Yesterday)", f"{latest['total_load']:,.0f} MWh")
    col2.metric("Days of Data", len(daily))

    st.line_chart(daily.sort_values("day").set_index("day")["total_load"])

    st.divider()

    st.subheader("Total Load by Country (1 Day, 7 Days, 30 Days)")
    country_summary = compute_total_load_by_country(load_df).rename(columns={
        'load_1d': 'Load (1 Day)',
        'load_7d': 'Load (7 Days)',
        'load_30d': 'Load (30 Days)'
    })
    st.dataframe(country_summary.style.format("{:,.0f}"), use_container_width=True)
