import pandas as pd
import plotly.express as px
from functools import lru_cache

@lru_cache(maxsize=4)
def load_data(path):
    df = pd.read_csv(path, parse_dates=['date'])
    # Ensure sales is numeric
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce').fillna(0)
    return df

def total_sales_by_category(df):
    grouped = df.groupby('category', dropna=False)['sales'].sum().reset_index()
    return grouped

def monthly_trend(df):
    # Ensure we have a month column derived from datetime
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['month'] = df['date'].dt.to_period('M').astype(str)
    trend = df.groupby('month')['sales'].sum().reset_index().sort_values('month')
    return trend

def generate_bar_chart(grouped_df):
    fig = px.bar(grouped_df, x='category', y='sales', title='Sales by Category')
    fig.update_traces(hovertemplate='Category=%{x}<br>Sales=%{y:.2f}')
    return fig

def generate_line_chart(trend_df):
    fig = px.line(trend_df, x='month', y='sales', title='Monthly Sales Trend')
    return fig
