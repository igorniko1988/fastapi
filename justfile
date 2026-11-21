dev port="8000":
    uv run uvicorn app.main:app --reload --port {{port}}

prod:
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

lint:
    uv run ruff check --fix

format:
    uv run ruff format