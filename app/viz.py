import pandas as pd
import plotly.express as px

def load_data(path):
    # BUG: parse_dates is False and date column left as string; also silent on missing file
    df = pd.read_csv(path)
    return df

def total_sales_by_category(df):
    # BUG: if sales column is string, this concatenates; also doesn't handle missing categories
    grouped = df.groupby('category')['sales'].sum().reset_index()
    return grouped

def monthly_trend(df):
    # BUG: tries to group by 'month' which doesn't exist; also uses string slicing incorrectly
    df['month'] = df['date'].apply(lambda x: x[:7])  # if datetime, this fails; if string OK
    trend = df.groupby('month')['sales'].sum().reset_index()
    return trend

def generate_bar_chart(grouped_df):
    # BUG: missing hover info and using wrong labels
    fig = px.bar(grouped_df, x='category', y='sales', title='Sales by Category')
    # Intentionally remove hovertemplate to simulate missing tooltip behavior
    return fig

def generate_line_chart(trend_df):
    fig = px.line(trend_df, x='month', y='sales', title='Monthly Sales Trend')
    return fig
