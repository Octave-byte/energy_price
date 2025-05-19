import pandas as pd
import requests
import os
from datetime import datetime, timedelta

# Airtable API configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "")

# Tables in Airtable
TABLES = {
    "price": os.getenv("AIRTABLE_PRICE_TABLE_ID", ""),
    "production": os.getenv("AIRTABLE_PRODUCTION_TABLE_ID", ""),
    "consumption": os.getenv("AIRTABLE_CONSUMPTION_TABLE_ID", ""),
    "transfer": os.getenv("AIRTABLE_TRANSFER_TABLE_ID", "")
}

def fetch_airtable_data(table_name):
    """
    Fetch data from a specific Airtable table
    """
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID or not TABLES[table_name]:
        raise ValueError(f"Airtable configuration for {table_name} is incomplete")
    
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLES[table_name]}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    all_records = []
    params = {}
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from Airtable: {response.text}")
        
        data = response.json()
        all_records.extend(data.get('records', []))
        
        # Check for pagination
        offset = data.get('offset')
        if offset:
            params = {'offset': offset}
        else:
            break
    
    # Convert to DataFrame
    df = pd.DataFrame([record['fields'] for record in all_records])
    
    # Convert date strings to datetime objects if applicable
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return df

def fetch_all_data():
    """
    Fetch all required data from Airtable
    """
    data = {}
    
    for table_name in TABLES.keys():
        try:
            data[table_name] = fetch_airtable_data(table_name)
        except Exception as e:
            print(f"Error fetching {table_name} data: {e}")
            data[table_name] = pd.DataFrame()  # Empty DataFrame as fallback
    
    return data

def get_cached_data(cached_data):
    """
    Return cached data or fetch new data if not available
    """
    if cached_data is None:
        return fetch_all_data()
    return cached_data

def filter_last_n_days(df, days=30, date_column='date'):
    """
    Filter dataframe to include only the last n days of data
    """
    if df.empty or date_column not in df.columns:
        return df
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    return df[df[date_column] >= start_date]

def get_price_data(data, days=30):
    """
    Get price data for the specified number of days
    """
    if data is None or 'price' not in data or data['price'].empty:
        return pd.DataFrame()
    
    return filter_last_n_days(data['price'], days)

def get_production_data(data, days=30):
    """
    Get production data for the specified number of days
    """
    if data is None or 'production' not in data or data['production'].empty:
        return pd.DataFrame()
    
    return filter_last_n_days(data['production'], days)

def get_consumption_data(data, days=30):
    """
    Get consumption data for the specified number of days
    """
    if data is None or 'consumption' not in data or data['consumption'].empty:
        return pd.DataFrame()
    
    return filter_last_n_days(data['consumption'], days)

def get_transfer_data(data):
    """
    Get transfer data
    """
    if data is None or 'transfer' not in data or data['transfer'].empty:
        return pd.DataFrame()
    
    return data['transfer']
