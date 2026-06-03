#!/bin/bash
set -e

export PATH="/root/.local/bin:$PATH"

cd /app

echo "Applying database migrations..."
uv run alembic upgrade head

# Запускаем воркер в фоне
nohup uv run python -m bin.outbox &

# Запускаем API
exec uv run python -m bin.api
