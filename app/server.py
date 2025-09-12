from flask import Flask
from app.viz import load_data, total_sales_by_category, monthly_trend, generate_bar_chart, generate_line_chart
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    # Load data from the correct path within the repository
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_sales.csv')
    df = load_data(data_path)
    cat = total_sales_by_category(df)
    trend = monthly_trend(df)
    bar = generate_bar_chart(cat)
    line = generate_line_chart(trend)
    bar_html = bar.to_html(include_plotlyjs='cdn', full_html=False)
    line_html = line.to_html(include_plotlyjs=False, full_html=False)
    return f"<h1>Dashboard</h1><div>{bar_html}</div><div>{line_html}</div>"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
