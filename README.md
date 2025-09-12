# Complex Visualization Repo (with intentional bugs)

This repository is designed to test model abilities to fix visualization pipelines and server issues.

Structure:
- app/: visualization and server code (contains deliberate bugs)
- data/: sample_sales.csv
- tests/: pytest tests that exercise the viz functions

Run tests:
```
pytest -q
```

Start server:
```
python -m app.server
```
