##################################
### Energy Production
##################################

from datetime import timedelta
import pandas as pd

def compute_mix_breakdown_by_country(prod_df: pd.DataFrame) -> pd.DataFrame:
    d1 = pd.Timestamp.now(tz='UTC') - timedelta(days=1)

    df1 = prod_df[prod_df['datetime'] >= d1].copy()

    breakdown_cols = [
        'biomass', 'hydro_pumped_storage', 'hydro_run_of_river_and_poundage',
        'hydro_water_reservoir', 'other_renewable', 'solar', 'wind_onshore', 'wind_offshore'
    ]
    nuclear_col = ['nuclear']
    other_cols = [
        'fossil_gas', 'fossil_oil', 'fossil_hard_coal', 'other', 'waste', 'energy_storage'
    ]

    df1['renewables'] = df1[breakdown_cols].sum(axis=1)
    df1['nuclear'] = df1[nuclear_col].sum(axis=1)
    df1['other'] = df1[other_cols].sum(axis=1)

    grouped = df1.groupby(['country_name'])[['renewables', 'nuclear', 'other']].sum()
    grouped['total'] = grouped.sum(axis=1)
    grouped.reset_index(inplace=True)
    return grouped

# Function 2: europe_weighted_energy_mix_30d
def compute_weighted_mix_daily(prod_df: pd.DataFrame) -> pd.DataFrame:
    d30 = pd.Timestamp.now(tz='UTC') - timedelta(days=30)
    df = prod_df[prod_df['datetime'] >= d30].copy()

    breakdown_cols = [
        'biomass', 'hydro_pumped_storage', 'hydro_run_of_river_and_poundage',
        'hydro_water_reservoir', 'other_renewable', 'solar', 'wind_onshore', 'wind_offshore'
    ]
    nuclear_col = ['nuclear']
    other_cols = [
        'fossil_gas', 'fossil_oil', 'fossil_hard_coal', 'other', 'waste', 'energy_storage'
    ]

    df['date'] = df['datetime'].dt.date
    df['renewables'] = df[breakdown_cols].sum(axis=1)
    df['nuclear'] = df[nuclear_col].sum(axis=1)
    df['other'] = df[other_cols].sum(axis=1)

    daily = df.groupby('date')[['renewables', 'nuclear', 'other']].sum()
    daily['total'] = daily.sum(axis=1)
    daily['pct_renewables'] = 100 * daily['renewables'] / daily['total']
    daily['pct_nuclear'] = 100 * daily['nuclear'] / daily['total']
    daily['pct_other'] = 100 * daily['other'] / daily['total']
    daily.reset_index(inplace=True)
    return daily

# Function 3: energy_total_production_by_country
def compute_total_production_by_country(prod_df: pd.DataFrame) -> pd.DataFrame:
    now = pd.Timestamp.now(tz='UTC')
    d1 = now - timedelta(days=1)
    d7 = now - timedelta(days=7)
    d30 = now - timedelta(days=30)

    total_cols = [
        'biomass', 'geothermal', 'hydro_pumped_storage', 'hydro_run_of_river_and_poundage',
        'hydro_water_reservoir', 'other_renewable', 'solar', 'wind_onshore', 'wind_offshore',
        'nuclear', 'fossil_gas', 'fossil_oil', 'fossil_hard_coal', 'other', 'waste', 'energy_storage'
    ]

    grouped = prod_df.groupby(['country_name'])

    summary = grouped.apply(lambda g: pd.Series({
        'total_1d': g.loc[g['datetime'] >= d1, total_cols].sum().sum(),
        'total_7d': g.loc[g['datetime'] >= d7, total_cols].sum().sum(),
        'total_30d': g.loc[g['datetime'] >= d30, total_cols].sum().sum(),
    })).reset_index()
    return summary



##################################
### Energy Load
##################################


# 1. Daily Total Load Over Last 30 Days
def compute_daily_total_load_30d(load_df: pd.DataFrame) -> pd.DataFrame:
    d30 = pd.Timestamp.now(tz='UTC') - timedelta(days=30)
    df = load_df[load_df['datetime'] >= d30].copy()
    df['day'] = df['datetime'].dt.floor('D')
    daily_load = df.groupby('day')['actual_load'].sum().reset_index(name='total_load')
    return daily_load.sort_values('day', ascending=False)

# 2. Total Load Per Country Over 1, 7, 30 Days
def compute_total_load_by_country(load_df: pd.DataFrame) -> pd.DataFrame:
    now = pd.Timestamp.now(tz='UTC')
    d1, d7, d30 = now - timedelta(days=1), now - timedelta(days=7), now - timedelta(days=30)
    
    grouped = load_df.groupby(['country_name'])

    summary = grouped.apply(lambda g: pd.Series({
        'load_1d': g.loc[g['datetime'] >= d1, 'actual_load'].sum(),
        'load_7d': g.loc[g['datetime'] >= d7, 'actual_load'].sum(),
        'load_30d': g.loc[g['datetime'] >= d30, 'actual_load'].sum(),
    })).reset_index()
    return summary

##################################
### Energy Price
##################################

# 3. Average Price Per Country Over 1, 7, 30 Days
def compute_avg_price_by_country(price_df: pd.DataFrame) -> pd.DataFrame:
    now = pd.Timestamp.now(tz='UTC')
    d1, d7, d30 = now - timedelta(days=1), now - timedelta(days=7), now - timedelta(days=30)

    grouped = price_df.groupby(['country_name'])

    summary = grouped.apply(lambda g: pd.Series({
        'avg_1d': g.loc[g['datetime'] >= d1, 'price'].mean(),
        'avg_7d': g.loc[g['datetime'] >= d7, 'price'].mean(),
        'avg_30d': g.loc[g['datetime'] >= d30, 'price'].mean(),
    })).reset_index()
    return summary

# 4. Price Volatility Per Country (Standard Deviation)
def compute_price_volatility_by_country(price_df: pd.DataFrame) -> pd.DataFrame:
    now = pd.Timestamp.now(tz='UTC')
    d1, d7, d30 = now - timedelta(days=1), now - timedelta(days=7), now - timedelta(days=30)

    grouped = price_df.groupby(['country_name'])

    summary = grouped.apply(lambda g: pd.Series({
        'std_1d': g.loc[g['datetime'] >= d1, 'price'].std(),
        'std_7d': g.loc[g['datetime'] >= d7, 'price'].std(),
        'std_30d': g.loc[g['datetime'] >= d30, 'price'].std(),
    })).reset_index()
    return summary

# 5. Price Percentile Ranking By Country
def compute_price_percentile_by_country(price_df: pd.DataFrame) -> pd.DataFrame:
    d7 = pd.Timestamp.now(tz='UTC') - timedelta(days=7)
    recent_avg = price_df[price_df['datetime'] >= d7].groupby(
        ['country_code', 'country_name']
    )['price'].mean().reset_index(name='avg_price')

    recent_avg['price_percentile'] = recent_avg['avg_price'].rank(pct=True) * 100
    return recent_avg

# 6. Europe-Wide Weighted Average Price
def compute_weighted_avg_price_europe(price_df: pd.DataFrame, load_df: pd.DataFrame) -> pd.DataFrame:
    d30 = pd.Timestamp.now(tz='UTC') - timedelta(days=30)

    # Merge price and load
    merged = pd.merge(
        price_df[['datetime', 'country_code', 'price']],
        load_df[['datetime', 'country_code', 'actual_load']],
        on=['datetime', 'country_code'],
        how='inner'
    )

    merged = merged[merged['datetime'] >= d30].copy()

    def get_period(ts):
        now = pd.Timestamp.now(tz='UTC')
        if ts >= now - timedelta(days=1):
            return '1d'
        elif ts >= now - timedelta(days=7):
            return '7d'
        else:
            return '30d'

    merged['period'] = merged['datetime'].apply(get_period)
    grouped = merged.groupby('period').apply(
        lambda g: pd.Series({
            'weighted_sum': (g['price'] * g['actual_load']).sum(),
            'total_load': g['actual_load'].sum()
        })
    ).reset_index()

    grouped['weighted_avg_price'] = grouped['weighted_sum'] / grouped['total_load']
    return grouped[['period', 'weighted_avg_price']]
