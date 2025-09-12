import pandas as pd
import plotly.express as px

def load_data(path):
    # Fixed: proper date parsing and error handling
    try:
        df = pd.read_csv(path, parse_dates=['date'])
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {path}")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV file: {e}")

def total_sales_by_category(df):
    # Fixed: ensure sales is numeric and handle missing categories properly
    df = df.copy()
    # Convert sales to numeric, handling any string values
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    # Remove any rows with NaN sales values
    df = df.dropna(subset=['sales'])
    # Group and sum, ensuring we have all categories
    grouped = df.groupby('category')['sales'].sum().reset_index()
    # Sort by sales for better visualization
    grouped = grouped.sort_values('sales', ascending=False)
    return grouped

def monthly_trend(df):
    # Fixed: handle both datetime and string date formats properly
    df = df.copy()  # Don't modify original dataframe
    if df['date'].dtype == 'object':
        # If date is string, use string slicing
        df['month'] = df['date'].apply(lambda x: x[:7])
    else:
        # If date is datetime, use proper datetime formatting
        df['month'] = df['date'].dt.strftime('%Y-%m')
    trend = df.groupby('month')['sales'].sum().reset_index()
    return trend

def generate_bar_chart(grouped_df):
    # Fixed: proper hover info and improved styling
    fig = px.bar(
        grouped_df, 
        x='category', 
        y='sales', 
        title='Sales by Category',
        labels={'sales': 'Total Sales ($)', 'category': 'Product Category'},
        hover_data={'sales': ':,.2f'}
    )
    # Ensure interactive tooltips work properly
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>' +
                      'Total Sales: $%{y:,.2f}<br>' +
                      '<extra></extra>'
    )
    return fig

def generate_line_chart(trend_df):
    # Improved: better styling and hover information
    fig = px.line(
        trend_df, 
        x='month', 
        y='sales', 
        title='Monthly Sales Trend',
        labels={'sales': 'Total Sales ($)', 'month': 'Month'},
        hover_data={'sales': ':,.2f'}
    )
    # Enhanced styling and hover
    fig.update_traces(
        line=dict(width=3),
        hovertemplate='<b>%{x}</b><br>' +
                      'Total Sales: $%{y:,.2f}<br>' +
                      '<extra></extra>'
    )
    fig.update_layout(
        hovermode='x unified'
    )
    return fig
