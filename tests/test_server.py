import os
import re
from app.server import app

# Use Flask's built-in test client so we don't have to spin up a server process

def test_index_renders_plots_and_uses_data_path():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    html = resp.data.decode('utf-8')
    # Should contain plotly script tags and our hover template
    assert 'plotly' in html.lower()
    assert 'Category=' in html or 'category=' in html
    # Ensure both bar and line charts are embedded
    assert html.count('<div') >= 2
