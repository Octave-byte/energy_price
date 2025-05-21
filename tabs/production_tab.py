import streamlit as st
from utils.helpers import (
    compute_mix_breakdown_by_country,
    compute_weighted_mix_daily,
    compute_total_production_by_country
)

def render(prod_df):
    st.subheader("Production Mix by Country (Last 1 Day)")
    st.dataframe(compute_mix_breakdown_by_country(prod_df), use_container_width=True)

    st.subheader("Daily Europe-wide Production Mix (Last 30 Days)")
    st.line_chart(compute_weighted_mix_daily(prod_df).set_index("date")[["pct_renewables", "pct_nuclear", "pct_other"]])

    st.subheader("Total Production by Country (1d, 7d, 30d)")
    st.dataframe(compute_total_production_by_country(prod_df), use_container_width=True)
