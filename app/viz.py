import pandas as pd
import plotly.express as px

def load_data(path):
    df = pd.read_csv(path, parse_dates=['date'])
    # Ensure numeric sales for aggregations
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce').fillna(0)
    return df

def total_sales_by_category(df):
    # Ensure numeric sales for correct aggregation
    df = df.copy()
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce').fillna(0)
    grouped = df.groupby('category', as_index=False)['sales'].sum()
    return grouped

def monthly_trend(df):
    # Create year-month column regardless of dtype
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['month'] = df['date'].dt.strftime('%Y-%m')
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce').fillna(0)
    trend = df.groupby('month', as_index=False)['sales'].sum().sort_values('month')
    return trend

def generate_bar_chart(grouped_df):
    fig = px.bar(grouped_df, x='category', y='sales', title='Sales by Category', labels={'category': 'Category', 'sales': 'Sales'})
    fig.update_traces(hovertemplate='Category: %{x}<br>Sales: %{y:.2f}<extra></extra>')
    return fig

def generate_line_chart(trend_df):
    fig = px.line(trend_df, x='month', y='sales', title='Monthly Sales Trend')
    return fig
