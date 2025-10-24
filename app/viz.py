import pandas as pd
import plotly.express as px

def load_data(path):
    """Load data from CSV file with proper date parsing and error handling."""
    try:
        df = pd.read_csv(path, parse_dates=['date'])
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {path}")
    except Exception as e:
        raise Exception(f"Error loading data from {path}: {e}")

def total_sales_by_category(df):
    """Aggregate total sales by category with proper numeric handling."""
    # Ensure sales column is numeric
    df = df.copy()
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    grouped = df.groupby('category')['sales'].sum().reset_index()
    return grouped

def monthly_trend(df):
    """Calculate monthly sales trend with proper datetime handling."""
    df = df.copy()
    # Ensure sales column is numeric
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    # Extract year-month from datetime
    df['month'] = df['date'].dt.to_period('M').astype(str)
    trend = df.groupby('month')['sales'].sum().reset_index()
    return trend

def generate_bar_chart(grouped_df):
    """Generate bar chart with interactive tooltips."""
    fig = px.bar(grouped_df, x='category', y='sales', 
                 title='Sales by Category',
                 labels={'sales': 'Total Sales ($)', 'category': 'Category'},
                 hover_data={'sales': ':.2f'})
    # Customize hover template for better interactivity
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>')
    return fig

def generate_line_chart(trend_df):
    fig = px.line(trend_df, x='month', y='sales', title='Monthly Sales Trend')
    return fig
