import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import pytest
from app.viz import (
    generate_bar_chart,
    generate_line_chart,
    load_data,
    monthly_trend,
    total_sales_by_category,
)

DATA_PATH = ROOT / 'data' / 'sample_sales.csv'


def test_load_data_columns_and_types():
    df = load_data(DATA_PATH)
    assert {'date', 'category', 'sales'} <= set(df.columns)
    assert pd.api.types.is_datetime64_any_dtype(df['date'])
    assert pd.api.types.is_numeric_dtype(df['sales'])

def test_total_sales_by_category():
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    assert set(grouped['category']) == {'Electronics', 'Books', 'Furniture', 'Clothing'}
    assert all(grouped['sales'] > 0)
    assert grouped['sales'].dtype.kind in 'fi'


def test_total_sales_by_category_matches_raw_sum():
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    expected = (
        df.groupby('category')['sales']
        .sum()
        .reset_index()
        .sort_values('sales', ascending=False)
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(grouped, expected)


def test_monthly_trend():
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    assert list(trend['month']) == sorted(trend['month'])
    assert all(trend['sales'] >= 0)
    expected = (
        df.groupby(df['date'].dt.to_period('M'))['sales']
        .sum()
        .reset_index()
    )
    expected['month'] = expected['date'].dt.strftime('%Y-%m')
    expected = expected.drop(columns=['date']).sort_values('month').reset_index(drop=True)
    expected = expected[['month', 'sales']]
    pd.testing.assert_frame_equal(trend.reset_index(drop=True), expected)


def test_load_data_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(tmp_path / 'missing.csv')


def test_generate_bar_chart_hover():
    df = load_data(DATA_PATH)
    grouped = total_sales_by_category(df)
    fig = generate_bar_chart(grouped)
    trace = fig.data[0]
    assert "Sales" in trace.hovertemplate
    assert "%{y:,.2f}" in trace.hovertemplate
    assert trace.hovertemplate.endswith("<extra></extra>")




def test_generate_line_chart_ordering():
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    fig = generate_line_chart(trend)
    x_values = list(fig.data[0].x)
    assert x_values == sorted(x_values)
