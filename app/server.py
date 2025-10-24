from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template

from app.viz import (
    generate_bar_chart,
    generate_line_chart,
    load_data,
    monthly_trend,
    total_sales_by_category,
)

_BASE_DIR = Path(__file__).resolve().parent.parent
_DATA_PATH = _BASE_DIR / "data" / "sample_sales.csv"
_TEMPLATE_DIR = _BASE_DIR / "templates"
_STATIC_DIR = _BASE_DIR / "static"

app = Flask(
    __name__,
    template_folder=str(_TEMPLATE_DIR),
    static_folder=str(_STATIC_DIR),
)


def _build_figures():
    df = load_data(_DATA_PATH)
    category_summary = total_sales_by_category(df)
    trend_summary = monthly_trend(df)
    bar_fig = generate_bar_chart(category_summary)
    line_fig = generate_line_chart(trend_summary)
    return bar_fig, line_fig


@app.route("/")
def index():
    bar_fig, line_fig = _build_figures()
    bar_html = bar_fig.to_html(full_html=False, include_plotlyjs="cdn")
    line_html = line_fig.to_html(full_html=False, include_plotlyjs=False)
    return render_template(
        "index.html",
        title="Sales Dashboard",
        bar_chart=bar_html,
        line_chart=line_html,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
