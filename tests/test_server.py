import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.server import _DATA_PATH, _build_figures, app


@pytest.fixture()
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_data_path_exists():
    assert _DATA_PATH.exists()


def test_build_figures_returns_plotly_objects():
    bar, line = _build_figures()
    assert bar.data and line.data
    assert "Sales" in bar.data[0].hovertemplate
    assert bar.data[0].hovertemplate.endswith("<extra></extra>")


def test_index_route_renders_dashboard(client):
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Sales Dashboard" in html
    assert "Plotly.newPlot" in html
    assert "category-bar" in html and "trend-line" in html
    assert "Sales by Category" in html
    assert "Monthly Sales Trend" in html

