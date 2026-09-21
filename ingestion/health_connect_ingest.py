import argparse
import hashlib
import os
from dotenv import load_dotenv
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


HEALTH_CONNECT_TABLES = [
    'active_calories_burned_record_table',
    'activity_date_table',
    'weight_record_table',
    'total_calories_burned_record_table',
    'steps_record_table',
    'StepsCadenceRecordTable',
    'steps_cadence_record_table',
    'SpeedRecordTable',
    'speed_record_table',
    'sleep_stages_table',
    'sleep_session_record_table',
    'resting_heart_rate_record_table',
    'read_access_logs_table',
    'preference_table',
    'heart_rate_record_series_table',
    'oxygen_saturation_record_table',
    'height_record_table',
    'nutrition_record_table',
    'heart_rate_record_table',
    'health_data_category_priority_table',
    'exercise_session_record_table',
    'exercise_segments_table',
    'exercise_route_table',
    'distance_record_table',
    'device_info_table',
    'device_data_sources_table',
    'body_fat_record_table',
    'basal_metabolic_rate_record_table',
    'application_info_table'
]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / "infrastructure" / ".env"

load_dotenv(ENV_FILE)
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
BRONZE_SCHEMA = "bronze"


def calculate_file_hash(path: Path) -> str:
    """Calculate SHA-256 hash of source SQLite database."""
    sha256 = hashlib.sha256()

    with path.open("rb") as f:
        while chunk := f.read(1024 * 1024):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_engine_connection():
    return create_engine(
        f"postgresql+psycopg2://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


def create_ingestion_table(engine):
    """Create metadata table for ingestion batches."""

    with engine.begin() as conn:
        conn.execute(text(f"""
            CREATE SCHEMA IF NOT EXISTS {BRONZE_SCHEMA};
        """))

        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {BRONZE_SCHEMA}.ingestion_batches (
                batch_id UUID PRIMARY KEY,
                source_file TEXT NOT NULL,
                source_file_hash TEXT NOT NULL,
                loaded_at TIMESTAMPTZ NOT NULL,
                status TEXT NOT NULL,
                tables_loaded INTEGER,
                rows_loaded BIGINT,
                error_message TEXT
            );
        """))


def create_batch(engine, batch_id, source_file, source_file_hash, loaded_at):
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                INSERT INTO {BRONZE_SCHEMA}.ingestion_batches (
                    batch_id,
                    source_file,
                    source_file_hash,
                    loaded_at,
                    status,
                    tables_loaded,
                    rows_loaded
                )
                VALUES (
                    :batch_id,
                    :source_file,
                    :source_file_hash,
                    :loaded_at,
                    'running',
                    0,
                    0
                );
            """),
            {
                "batch_id": batch_id,
                "source_file": source_file,
                "source_file_hash": source_file_hash,
                "loaded_at": loaded_at,
            },
        )


def update_batch_success(engine, batch_id, tables_loaded, rows_loaded):
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                UPDATE {BRONZE_SCHEMA}.ingestion_batches
                SET
                    status = 'success',
                    tables_loaded = :tables_loaded,
                    rows_loaded = :rows_loaded
                WHERE batch_id = :batch_id;
            """),
            {
                "batch_id": batch_id,
                "tables_loaded": tables_loaded,
                "rows_loaded": rows_loaded,
            },
        )


def update_batch_failed(engine, batch_id, error_message):
    with engine.begin() as conn:
        conn.execute(
            text(f"""
                UPDATE {BRONZE_SCHEMA}.ingestion_batches
                SET
                    status = 'failed',
                    error_message = :error_message
                WHERE batch_id = :batch_id;
            """),
            {
                "batch_id": batch_id,
                "error_message": str(error_message),
            },
        )


def ingest(source_db: Path):

    if not source_db.exists():
        raise FileNotFoundError(
            f"Source database does not exist: {source_db}"
        )

    print(f"Source: {source_db}")

    loaded_at = datetime.now(timezone.utc)
    batch_id = uuid.uuid4()
    source_hash = calculate_file_hash(source_db)

    print(f"Batch ID: {batch_id}")
    print(f"Source SHA-256: {source_hash}")
    print(f"Loaded at: {loaded_at.isoformat()}")

    engine = create_engine_connection()

    create_ingestion_table(engine)

    create_batch(
        engine,
        batch_id,
        source_db.name,
        source_hash,
        loaded_at,
    )

    total_rows = 0
    tables_loaded = 0

    try:

        with sqlite3.connect(source_db) as sqlite_conn:

            for table in HEALTH_CONNECT_TABLES:

                print(f"\n Loading {table}")

                # Read entire SQLite table.
                df = pd.read_sql_query(
                    f'SELECT * FROM "{table}"',
                    sqlite_conn,
                )
                row_count = len(df)

                # Add metadata columns for ingestion tracking.
                df["loaded_at"] = loaded_at
                df["batch_id"] = batch_id
                df["source_file"] = source_db.name
                target_table = table

                # Load to PostgreSQL bronze schema.
                df.to_sql(
                    target_table,
                    engine,
                    schema=BRONZE_SCHEMA,
                    if_exists="append",
                    index=False,
                    chunksize=5000,
                )

                print(
                    f" Success: {row_count:,} source rows "
                    f"loaded into bronze.{target_table}"
                )

                total_rows += row_count
                tables_loaded += 1

        update_batch_success(
            engine,
            batch_id,
            tables_loaded,
            total_rows,
        )

        print("\n========================================")
        print("INGESTION SUCCESS")
        print("========================================")
        print(f"Tables: {tables_loaded}")
        print(f"Rows:   {total_rows:,}")
        print(f"Batch:  {batch_id}")

    except Exception as e:

        update_batch_failed(
            engine,
            batch_id,
            e,
        )

        print("\n========================================")
        print("INGESTION FAILED")
        print("========================================")
        print(str(e))

        raise


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Load Health Connect SQLite tables into PostgreSQL bronze layer."
    )

    parser.add_argument(
        "source_db",
        type=Path,
        help="Path to Health Connect .db file",
    )

    args = parser.parse_args()

    ingest(args.source_db)