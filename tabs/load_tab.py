import streamlit as st
from utils.helpers import (
    compute_daily_total_load_30d,
    compute_total_load_by_country
)

def render(load_df):
    st.subheader("Daily Total Load (Last 30 Days)")
    st.line_chart(compute_daily_total_load_30d(load_df).set_index("day"))

    st.subheader("Total Load by Country (1d, 7d, 30d)")
    st.dataframe(compute_total_load_by_country(load_df), use_container_width=True)
