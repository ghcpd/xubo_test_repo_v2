import os
import pandas as pd
import pytest
from app.viz import load_data, total_sales_by_category, monthly_trend

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sales.csv')

def test_load_data():
    df = load_data(DATA_PATH)
    assert 'date' in df.columns
    assert 'category' in df.columns
    assert 'sales' in df.columns

def test_total_sales_by_category():
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    # Expect one row per category
    assert set(grouped['category']) == set(['Electronics','Books','Furniture','Clothing'])
    # aggregated sales should be positive numbers
    assert all(grouped['sales'] > 0)

def test_monthly_trend():
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    # Expect month column like '2023-01'
    assert 'month' in trend.columns
    assert all(trend['sales'] >= 0)
