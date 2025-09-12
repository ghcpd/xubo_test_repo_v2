from flask import Flask, render_template, send_file
from app.viz import load_data, total_sales_by_category, monthly_trend, generate_bar_chart, generate_line_chart
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    # BUG: wrong data path (missing data/ prefix) leading to FileNotFoundError
    df = load_data('sample_sales.csv')
    cat = total_sales_by_category(df)
    trend = monthly_trend(df)
    bar = generate_bar_chart(cat)
    line = generate_line_chart(trend)
    # Return a simple page with placeholders (not rendering figures correctly)
    return f"<h1>Dashboard (broken)</h1><div>Bar: {bar.to_html()}</div><div>Line: {line.to_html()}</div>"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
