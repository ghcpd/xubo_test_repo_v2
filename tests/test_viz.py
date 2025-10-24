import os
import pandas as pd
import pytest
from app.viz import load_data, total_sales_by_category, monthly_trend, generate_bar_chart, generate_line_chart

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sales.csv')

def test_load_data():
    df = load_data(DATA_PATH)
    assert 'date' in df.columns
    assert 'category' in df.columns
    assert 'sales' in df.columns

def test_load_data_datetime_parsing():
    """Test that date column is parsed as datetime."""
    df = load_data(DATA_PATH)
    assert pd.api.types.is_datetime64_any_dtype(df['date']), "Date column should be datetime type"

def test_load_data_file_not_found():
    """Test that FileNotFoundError is raised for missing files."""
    with pytest.raises(FileNotFoundError, match="Data file not found"):
        load_data('nonexistent_file.csv')

def test_total_sales_by_category():
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    # Expect one row per category
    assert set(grouped['category']) == set(['Electronics','Books','Furniture','Clothing'])
    # aggregated sales should be positive numbers
    assert all(grouped['sales'] > 0)

def test_total_sales_by_category_numeric():
    """Test that sales aggregation returns numeric values."""
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    assert pd.api.types.is_numeric_dtype(grouped['sales']), "Aggregated sales should be numeric"
    assert grouped['sales'].dtype in ['float64', 'int64'], "Sales should be float or int"

def test_monthly_trend():
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    # Expect month column like '2023-01'
    assert 'month' in trend.columns
    assert all(trend['sales'] >= 0)

def test_monthly_trend_format():
    """Test that monthly trend produces correct month format."""
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    # Check that month format is correct (YYYY-MM)
    import re
    for month in trend['month']:
        assert re.match(r'^\d{4}-\d{2}$', str(month)), f"Month {month} should be in YYYY-MM format"

def test_generate_bar_chart_hover():
    """Test that bar chart has proper hover configuration."""
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    fig = generate_bar_chart(grouped)
    
    # Check that figure has data
    assert len(fig.data) > 0, "Bar chart should have data"
    
    # Check that hover template is configured
    assert fig.data[0].hovertemplate is not None, "Bar chart should have hover template"
    assert 'Sales' in fig.data[0].hovertemplate or '%{y' in fig.data[0].hovertemplate, \
        "Hover template should include sales information"

def test_generate_line_chart():
    """Test that line chart is generated successfully."""
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    fig = generate_line_chart(trend)
    
    # Check that figure has data
    assert len(fig.data) > 0, "Line chart should have data"
    assert fig.data[0].type == 'scatter', "Line chart should be scatter/line type"
