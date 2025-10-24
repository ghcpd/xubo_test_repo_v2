from flask import Flask, render_template, send_file
from app.viz import load_data, total_sales_by_category, monthly_trend, generate_bar_chart, generate_line_chart
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    # Fixed: correct data path with data/ prefix
    df = load_data('data/sample_sales.csv')
    cat = total_sales_by_category(df)
    trend = monthly_trend(df)
    bar = generate_bar_chart(cat)
    line = generate_line_chart(trend)
    # Render figures properly with better HTML structure
    # Use include_plotlyjs='cdn' for first chart only to avoid duplication
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sales Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            h1 {{ color: #333; text-align: center; }}
            .chart {{ margin: 20px auto; padding: 20px; background: white; 
                     border: 1px solid #ddd; border-radius: 8px; max-width: 1200px;
                     box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h2 {{ color: #555; margin-top: 0; }}
        </style>
    </head>
    <body>
        <h1>Sales Dashboard</h1>
        <div class="chart">
            <h2>Sales by Category</h2>
            {bar.to_html(include_plotlyjs='cdn', full_html=False, div_id='bar-chart')}
        </div>
        <div class="chart">
            <h2>Monthly Sales Trend</h2>
            {line.to_html(include_plotlyjs=False, full_html=False, div_id='line-chart')}
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(debug=True, port=5001)
