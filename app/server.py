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
    
    # Improved: Proper HTML rendering with better styling
    bar_html = bar.to_html(include_plotlyjs=True, div_id="bar-chart")
    line_html = line.to_html(include_plotlyjs=False, div_id="line-chart")
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sales Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
            .chart-section {{ margin: 30px 0; }}
            .chart-title {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #555; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sales Analytics Dashboard</h1>
            <div class="chart-section">
                <div class="chart-title">Sales by Category</div>
                {bar_html}
            </div>
            <div class="chart-section">
                <div class="chart-title">Monthly Sales Trend</div>
                {line_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

if __name__ == '__main__':
    app.run(debug=True, port=5001)
