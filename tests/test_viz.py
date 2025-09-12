import os
import pandas as pd
import pytest
from app.viz import load_data, total_sales_by_category, monthly_trend, generate_bar_chart, generate_line_chart
from app.server import index
import plotly.graph_objects as go

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sales.csv')

def test_load_data():
    df = load_data(DATA_PATH)
    assert 'date' in df.columns
    assert 'category' in df.columns
    assert 'sales' in df.columns
    # Test that dates are properly parsed as datetime
    assert df['date'].dtype == 'datetime64[ns]'

def test_load_data_file_not_found():
    # Test error handling for missing files
    with pytest.raises(FileNotFoundError, match="Data file not found"):
        load_data('nonexistent_file.csv')

def test_total_sales_by_category():
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    # Expect one row per category
    assert set(grouped['category']) == set(['Electronics','Books','Furniture','Clothing'])
    # aggregated sales should be positive numbers
    assert all(grouped['sales'] > 0)
    # Verify sales column is numeric
    assert grouped['sales'].dtype == 'float64'
    # Check that data is sorted by sales (descending)
    assert grouped['sales'].is_monotonic_decreasing

def test_total_sales_by_category_string_sales():
    # Test robustness with string sales values
    df = pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02'],
        'category': ['A', 'B'],
        'sales': ['100.5', '200.75']  # String sales values
    })
    grouped = total_sales_by_category(df)
    assert grouped['sales'].dtype == 'float64'
    assert grouped['sales'].sum() == 301.25

def test_monthly_trend():
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    # Expect month column like '2023-01'
    assert 'month' in trend.columns
    assert all(trend['sales'] >= 0)
    # Test that all months follow YYYY-MM format
    assert all(len(month) == 7 and month[4] == '-' for month in trend['month'])
    # Original dataframe should not be modified
    assert 'month' not in df.columns

def test_monthly_trend_string_dates():
    # Test with string dates (legacy compatibility)
    df = pd.DataFrame({
        'date': ['2023-01-01T00:00:00', '2023-01-02T00:00:00', '2023-02-01T00:00:00'],
        'category': ['A', 'B', 'A'],
        'sales': [100, 200, 150]
    })
    trend = monthly_trend(df)
    assert len(trend) == 2  # Two distinct months
    assert set(trend['month']) == {'2023-01', '2023-02'}

def test_generate_bar_chart():
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    fig = generate_bar_chart(grouped)
    
    # Check that it's a plotly figure
    assert isinstance(fig, go.Figure)
    # Check that hover template is properly configured
    assert fig.data[0].hovertemplate is not None
    assert '$%{y:,.2f}' in fig.data[0].hovertemplate
    # Check axis labels
    assert 'Total Sales' in fig.layout.yaxis.title.text
    assert 'Product Category' in fig.layout.xaxis.title.text

def test_generate_line_chart():
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    fig = generate_line_chart(trend)
    
    # Check that it's a plotly figure
    assert isinstance(fig, go.Figure)
    # Check that it has the correct title
    assert 'Monthly Sales Trend' in fig.layout.title.text

def test_server_index_integration():
    # Test the complete server integration
    response = index()
    assert isinstance(response, str)
    assert len(response) > 1000  # Should contain substantial HTML content
    assert 'Dashboard' in response
    assert 'Bar:' in response
    assert 'Line:' in response
    # Should contain plotly div elements
    assert 'plotly-graph-div' in response
