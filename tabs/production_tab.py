import streamlit as st
from utils.helpers import (
    compute_mix_breakdown_by_country,
    compute_weighted_mix_daily,
    compute_total_production_by_country
)

def render(prod_df):
    st.subheader("🌍 Europe-wide Production Overview")
    # KPI (top production countries last 1d)
    summary = compute_total_production_by_country(prod_df)
    top = summary.sort_values("total_1d", ascending=False).head(1)

    col1, col2 = st.columns(2)
    col1.metric("Top Producer (1 Day)", top.iloc[0]['country_name'], f"{top.iloc[0]['total_1d']:,.0f} MWh")
    col2.metric("Total Countries", summary['country_name'].nunique())

    st.divider()

    st.subheader("Production Breakdown by Country (Last 1 Day)")
    df_mix = compute_mix_breakdown_by_country(prod_df).rename(columns={
        'renewables': 'Renewables',
        'nuclear': 'Nuclear',
        'other': 'Other',
        'total': 'Total'
    })
    st.dataframe(df_mix.style.format("{:,.0f}"), use_container_width=True)

    st.divider()

    st.subheader("Europe-wide Daily Production Mix (Last 30 Days)")
    mix_daily = compute_weighted_mix_daily(prod_df)
    mix_daily.rename(columns={
        'pct_renewables': 'Renewables (%)',
        'pct_nuclear': 'Nuclear (%)',
        'pct_other': 'Other (%)'
    }, inplace=True)
    st.line_chart(mix_daily.set_index("date")[["Renewables (%)", "Nuclear (%)", "Other (%)"]])

    st.divider()

    st.subheader("Total Production by Country")
    summary = summary.rename(columns={
        'total_1d': 'Total (1 Day)',
        'total_7d': 'Total (7 Days)',
        'total_30d': 'Total (30 Days)'
    })
    st.dataframe(summary.style.format("{:,.0f}"), use_container_width=True)
