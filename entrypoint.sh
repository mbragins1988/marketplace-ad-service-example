#!/bin/bash
set -e

export PATH="/root/.local/bin:$PATH"

cd /app

echo "Applying database migrations..."
uv run alembic upgrade head

echo "Starting FastAPI application..."
exec uv run python -m bin.api
