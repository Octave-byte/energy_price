import streamlit as st
from data_loader import load_data
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
from tabs import price_tab, production_tab, load_tab

st.set_page_config(page_title="Energy Dashboard", layout="wide")

st.title("⚡ European Energy Dashboard")

prod_df, load_df, price_df = load_data()

tab1, tab2, tab3 = st.tabs(["💶 Price", "🔋 Production", "📊 Load / Consumption"])

with tab1:
    price_tab.render(price_df, load_df)

with tab2:
    production_tab.render(prod_df)

with tab3:
    load_tab.render(load_df)
