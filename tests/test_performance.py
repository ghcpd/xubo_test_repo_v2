import time
import os
import pandas as pd
from app.viz import load_data, total_sales_by_category, monthly_trend, generate_bar_chart, generate_line_chart

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sales.csv')

def test_performance_data_loading():
    """Test that data loading is reasonably fast"""
    start_time = time.time()
    df = load_data(DATA_PATH)
    end_time = time.time()
    
    # Should load in under 1 second for small data
    assert (end_time - start_time) < 1.0
    assert len(df) == 480  # Expected number of rows

def test_performance_aggregations():
    """Test that aggregations are fast"""
    df = load_data(DATA_PATH)
    
    # Test category aggregation performance
    start_time = time.time()
    cat = total_sales_by_category(df)
    end_time = time.time()
    assert (end_time - start_time) < 0.5  # Should be very fast
    
    # Test monthly trend performance
    start_time = time.time()
    trend = monthly_trend(df)
    end_time = time.time()
    assert (end_time - start_time) < 0.5  # Should be very fast

def test_performance_chart_generation():
    """Test that chart generation is reasonably fast"""
    df = load_data(DATA_PATH)
    cat = total_sales_by_category(df)
    trend = monthly_trend(df)
    
    # Test bar chart generation
    start_time = time.time()
    bar_fig = generate_bar_chart(cat)
    end_time = time.time()
    assert (end_time - start_time) < 2.0  # Should generate in under 2 seconds
    
    # Test line chart generation
    start_time = time.time()
    line_fig = generate_line_chart(trend)
    end_time = time.time()
    assert (end_time - start_time) < 2.0  # Should generate in under 2 seconds

def test_memory_efficiency():
    """Test that functions don't unnecessarily copy data"""
    df = load_data(DATA_PATH)
    original_id = id(df)
    
    # monthly_trend should not modify the original dataframe
    trend = monthly_trend(df)
    assert 'month' not in df.columns  # Original df should not have month column
    
    # total_sales_by_category should not modify the original dataframe
    cat = total_sales_by_category(df)
    assert id(df) == original_id  # Should still be the same object reference
    assert len(df) == 480  # Original length should be unchanged

def test_data_type_efficiency():
    """Test that data types are optimal for performance"""
    df = load_data(DATA_PATH)
    
    # Date should be datetime for efficient operations
    assert df['date'].dtype == 'datetime64[ns]'
    
    # Sales should be numeric for efficient aggregation
    assert pd.api.types.is_numeric_dtype(df['sales'])
    
    cat = total_sales_by_category(df)
    # Aggregated sales should be float64
    assert cat['sales'].dtype == 'float64'