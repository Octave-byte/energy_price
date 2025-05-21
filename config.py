import streamlit as st
SUPABASE_API_KEY = st.secrets["auth_token"]
SUPABASE_URL = 'https://qkonktvwcbfkehznugum.supabase.co'


HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}
