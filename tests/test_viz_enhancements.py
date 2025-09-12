import os
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

from app.viz import load_data, total_sales_by_category, monthly_trend, generate_bar_chart
from app.server import index

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sales.csv')


def test_load_data_parses_date_and_sales_numeric():
    df = load_data(DATA_PATH)
    assert is_datetime64_any_dtype(df['date'])
    assert is_numeric_dtype(df['sales'])


def test_monthly_trend_months_and_format():
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    expected_months = sorted(pd.to_datetime(df['date']).dt.strftime('%Y-%m').unique().tolist())
    actual_months = sorted(trend['month'].unique().tolist())
    assert actual_months == expected_months


def test_generate_bar_chart_has_hover():
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    fig = generate_bar_chart(grouped)
    assert len(fig.data) > 0
    assert hasattr(fig.data[0], 'hovertemplate')
    assert 'Category:' in fig.data[0].hovertemplate
    assert 'Sales:' in fig.data[0].hovertemplate


def test_server_index_renders_plots():
    html = index()
    assert 'Dashboard' in html
    assert 'Plotly.newPlot' in html
