import pytest
from app.server import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test that the index route loads successfully."""
    response = client.get('/')
    assert response.status_code == 200, "Index route should return 200 OK"


def test_index_contains_dashboard_title(client):
    """Test that the index page contains the dashboard title."""
    response = client.get('/')
    assert b'Sales Dashboard' in response.data, "Page should contain 'Sales Dashboard' title"


def test_index_contains_bar_chart(client):
    """Test that the index page contains the bar chart."""
    response = client.get('/')
    assert b'Sales by Category' in response.data, "Page should contain bar chart title"


def test_index_contains_line_chart(client):
    """Test that the index page contains the line chart."""
    response = client.get('/')
    assert b'Monthly Sales Trend' in response.data, "Page should contain line chart title"


def test_index_contains_plotly(client):
    """Test that the index page includes Plotly charts."""
    response = client.get('/')
    # Check for Plotly-specific elements
    assert b'plotly' in response.data.lower(), "Page should include Plotly visualization"
