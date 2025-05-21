import streamlit as st
SUPABASE_API_KEY = st.secrets["auth_token"]
SUPABASE_URL = st.secrets["url"]

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}
