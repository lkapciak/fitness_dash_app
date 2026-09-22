FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    dbt-core==1.12.5 \
    dbt-postgres==1.11.0

ENV DBT_PROFILES_DIR=/app

CMD ["dbt", "--version"]