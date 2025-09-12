import os
import pandas as pd
from app.viz import load_data, total_sales_by_category, monthly_trend, generate_bar_chart

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sales.csv')

def test_load_data_parses_date_and_numeric_sales():
    df = load_data(DATA_PATH)
    assert pd.api.types.is_datetime64_any_dtype(df['date'])
    assert pd.api.types.is_numeric_dtype(df['sales'])

def test_monthly_trend_uses_calendar_months():
    df = load_data(DATA_PATH)
    trend = monthly_trend(df)
    assert set(trend['month']).issuperset({'2023-01','2023-02','2023-03','2023-04'})

def test_bar_chart_has_interactive_hover_template():
    df = load_data(DATA_PATH)
    cat = total_sales_by_category(df)
    fig = generate_bar_chart(cat)
    # Plotly figures expose hovertemplate on traces
    hovertemplates = [t.hovertemplate for t in fig.data if hasattr(t, 'hovertemplate')]
    assert any('Category=' in ht and 'Sales=' in ht for ht in hovertemplates if ht)
