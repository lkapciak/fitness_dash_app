#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

# run the daily ingestion script
"$PROJECT_ROOT/.venv/bin/python" ingestion/daily_ingestion.py

cd "$PROJECT_ROOT/infrastructure"

# run dbt models
# staging
docker compose run --rm dbt dbt run --select staging

# marts
docker compose run --rm dbt dbt run --select marts