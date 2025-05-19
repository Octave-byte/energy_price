import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st

def plot_energy_price_line(df, title="Energy Price Trends in Europe (Last 30 Days)"):
    """
    Create a line chart for energy price trends
    """
    if df.empty or 'date' not in df.columns or 'price' not in df.columns:
        st.error("No price data available to display")
        return None
    
    fig = px.line(
        df, 
        x='date', 
        y='price',
        color='country',
        title=title,
        labels={'price': 'Price (€/MWh)', 'date': 'Date', 'country': 'Country'}
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (€/MWh)",
        legend_title="Country",
        hovermode="x unified"
    )
    
    return fig

def plot_country_price_bar(df, title="Current Energy Prices by Country"):
    """
    Create a bar chart for current energy prices by country
    """
    if df.empty or 'country' not in df.columns or 'price' not in df.columns:
        st.error("No price data available to display")
        return None
    
    # Get the most recent price for each country
    latest_prices = df.sort_values('date').groupby('country').last().reset_index()
    
    fig = px.bar(
        latest_prices,
        x='country',
        y='price',
        color='country',
        title=title,
        labels={'price': 'Price (€/MWh)', 'country': 'Country'}
    )
    
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Price (€/MWh)",
        showlegend=False
    )
    
    return fig

def create_price_comparison_table(df):
    """
    Create a table comparing prices today, 7 days ago, and 30 days ago
    """
    if df.empty or 'date' not in df.columns or 'price' not in df.columns or 'country' not in df.columns:
        st.error("No price data available to display")
        return None
    
    # Get current date for reference
    max_date = df['date'].max()
    
    # Calculate comparison dates
    today = max_date
    week_ago = max_date - pd.Timedelta(days=7)
    month_ago = max_date - pd.Timedelta(days=30)
    
    # Find closest dates in the dataset
    def get_closest_date(target_date):
        return df['date'].iloc[(df['date'] - target_date).abs().argsort()[0]]
    
    closest_today = get_closest_date(today)
    closest_week_ago = get_closest_date(week_ago)
    closest_month_ago = get_closest_date(month_ago)
    
    # Get prices for each date
    today_prices = df[df['date'] == closest_today][['country', 'price']].set_index('country')
    week_ago_prices = df[df['date'] == closest_week_ago][['country', 'price']].set_index('country')
    month_ago_prices = df[df['date'] == closest_month_ago][['country', 'price']].set_index('country')
    
    # Join the dataframes
    comparison = pd.concat([
        today_prices.rename(columns={'price': 'Today'}),
        week_ago_prices.rename(columns={'price': '7 Days Ago'}),
        month_ago_prices.rename(columns={'price': '30 Days Ago'})
    ], axis=1).reset_index()
    
    # Calculate change percentages
    comparison['7d Change %'] = ((comparison['Today'] - comparison['7 Days Ago']) / comparison['7 Days Ago'] * 100).round(2)
    comparison['30d Change %'] = ((comparison['Today'] - comparison['30 Days Ago']) / comparison['30 Days Ago'] * 100).round(2)
    
    # Format the price columns
    for col in ['Today', '7 Days Ago', '30 Days Ago']:
        comparison[col] = comparison[col].round(2)
    
    return comparison

def plot_energy_production_line(df, title="Energy Production in Europe (Last 30 Days)"):
    """
    Create a line chart for energy production trends with evolution of mix
    """
    if df.empty or 'date' not in df.columns:
        st.error("No production data available to display")
        return None
    
    # Identify energy source columns (assuming they're not date or country columns)
    energy_sources = [col for col in df.columns if col not in ['date', 'country', 'total_production']]
    
    if not energy_sources:
        st.error("No energy source data available")
        return None
    
    # Group by date and sum across countries
    df_grouped = df.groupby('date')[energy_sources].sum().reset_index()
    
    # Create stacked area chart
    fig = go.Figure()
    
    for source in energy_sources:
        fig.add_trace(go.Scatter(
            x=df_grouped['date'],
            y=df_grouped[source],
            mode='lines',
            stackgroup='one',
            name=source.capitalize(),
            hoverinfo='x+y',
            line=dict(width=0.5)
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Production (MWh)",
        hovermode="x unified",
        legend_title="Energy Source"
    )
    
    return fig

def create_energy_mix_table(df):
    """
    Create a table showing energy mix for each country
    """
    if df.empty or 'country' not in df.columns:
        st.error("No production data available to display")
        return None
    
    # Identify energy source columns
    energy_sources = [col for col in df.columns if col not in ['date', 'country', 'total_production']]
    
    if not energy_sources:
        st.error("No energy source data available")
        return None
    
    # Get the most recent data for each country
    latest_data = df.sort_values('date').groupby('country').last().reset_index()
    
    # Select only country and energy sources
    mix_table = latest_data[['country'] + energy_sources].copy()
    
    # Calculate percentages
    total_production = mix_table[energy_sources].sum(axis=1)
    
    for source in energy_sources:
        mix_table[f"{source}_pct"] = (mix_table[source] / total_production * 100).round(2)
    
    # Select only country and percentage columns for display
    result_columns = ['country'] + [f"{source}_pct" for source in energy_sources]
    result_df = mix_table[result_columns].rename(
        columns={f"{source}_pct": f"{source.capitalize()} (%)" for source in energy_sources}
    )
    
    return result_df

def plot_energy_mix_bar(df):
    """
    Create a bar chart showing energy mix for each country
    """
    if df.empty or 'country' not in df.columns:
        st.error("No production data available to display")
        return None
    
    # Identify energy source columns
    energy_sources = [col for col in df.columns if col not in ['date', 'country', 'total_production']]
    
    if not energy_sources:
        st.error("No energy source data available")
        return None
    
    # Get the most recent data for each country
    latest_data = df.sort_values('date').groupby('country').last().reset_index()
    
    # Melt the dataframe for easier plotting
    melted_df = pd.melt(
        latest_data,
        id_vars=['country'],
        value_vars=energy_sources,
        var_name='source',
        value_name='production'
    )
    
    # Calculate percentage
    country_totals = melted_df.groupby('country')['production'].transform('sum')
    melted_df['percentage'] = (melted_df['production'] / country_totals * 100).round(2)
    
    # Create the stacked bar chart
    fig = px.bar(
        melted_df,
        x='country',
        y='percentage',
        color='source',
        title="Energy Mix by Country (%)",
        labels={
            'country': 'Country',
            'percentage': 'Percentage (%)',
            'source': 'Energy Source'
        },
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Percentage (%)",
        legend_title="Energy Source",
        barmode='stack'
    )
    
    return fig

def plot_energy_consumption_line(df, title="Energy Consumption in Europe (Last 30 Days)"):
    """
    Create a line chart for energy consumption trends
    """
    if df.empty or 'date' not in df.columns or 'consumption' not in df.columns:
        st.error("No consumption data available to display")
        return None
    
    # Group by date and sum across countries
    df_grouped = df.groupby('date')['consumption'].sum().reset_index()
    
    fig = px.line(
        df_grouped,
        x='date',
        y='consumption',
        title=title,
        labels={'consumption': 'Consumption (MWh)', 'date': 'Date'}
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Consumption (MWh)",
        hovermode="x unified"
    )
    
    return fig

def plot_country_consumption_bar(df, title="Energy Consumption by Country"):
    """
    Create a bar chart for energy consumption by country
    """
    if df.empty or 'country' not in df.columns or 'consumption' not in df.columns:
        st.error("No consumption data available to display")
        return None
    
    # Get the most recent data for each country
    latest_data = df.sort_values('date').groupby('country')['consumption'].mean().reset_index()
    
    fig = px.bar(
        latest_data,
        x='country',
        y='consumption',
        color='country',
        title=title,
        labels={'consumption': 'Avg. Consumption (MWh)', 'country': 'Country'}
    )
    
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Average Consumption (MWh)",
        showlegend=False
    )
    
    return fig

def plot_country_correlation_matrix(df, title="Energy Transfer Correlation Matrix"):
    """
    Create a correlation matrix showing energy dependencies between countries
    """
    if df.empty or 'from_country' not in df.columns or 'to_country' not in df.columns or 'amount' not in df.columns:
        st.error("No transfer data available to display")
        return None
    
    # Create a pivot table of transfers
    pivot_df = df.pivot_table(
        index='from_country',
        columns='to_country',
        values='amount',
        aggfunc='sum',
        fill_value=0
    )
    
    # Create heatmap
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Importing Country", y="Exporting Country", color="Energy Transfer (MWh)"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale="Viridis",
        title=title
    )
    
    fig.update_layout(
        xaxis=dict(tickangle=45),
        height=600
    )
    
    return fig

def plot_energy_independence(consumption_df, transfer_df, title="Energy Independence by Country"):
    """
    Create a chart showing energy independence for each country
    """
    if (consumption_df.empty or transfer_df.empty or 
        'country' not in consumption_df.columns or 'consumption' not in consumption_df.columns or
        'to_country' not in transfer_df.columns or 'amount' not in transfer_df.columns):
        st.error("No data available to display")
        return None
    
    # Calculate total consumption for each country
    consumption_total = consumption_df.groupby('country')['consumption'].sum().reset_index()
    
    # Calculate total imports for each country
    imports = transfer_df.groupby('to_country')['amount'].sum().reset_index()
    imports.columns = ['country', 'imports']
    
    # Merge the dataframes
    merged_df = pd.merge(consumption_total, imports, on='country', how='left')
    merged_df['imports'] = merged_df['imports'].fillna(0)
    
    # Calculate independence ratio
    merged_df['independence_ratio'] = (1 - (merged_df['imports'] / merged_df['consumption'])) * 100
    merged_df['independence_ratio'] = merged_df['independence_ratio'].clip(0, 100)  # Clip between 0 and 100%
    
    # Sort by independence ratio
    merged_df = merged_df.sort_values('independence_ratio', ascending=False)
    
    # Create the bar chart
    fig = px.bar(
        merged_df,
        x='country',
        y='independence_ratio',
        color='independence_ratio',
        title=title,
        labels={
            'country': 'Country',
            'independence_ratio': 'Energy Independence (%)'
        },
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Energy Independence (%)",
        coloraxis_showscale=False
    )
    
    return fig
