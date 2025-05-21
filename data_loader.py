import streamlit as st
import pandas as pd
import requests
from config import SUPABASE_URL, HEADERS

@st.cache_data(ttl=86400)
def load_data():
    def fetch(endpoint):
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}?select=*"
        response = requests.get(url, headers=HEADERS)
        df = pd.DataFrame(response.json())
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.drop_duplicates(subset=["datetime", "country_name"])
        return df

    prod_df = fetch("energy_mix_mat")
    load_df = fetch("load_mat")
    price_df = fetch("price_mat")
    return prod_df, load_df, price_df
