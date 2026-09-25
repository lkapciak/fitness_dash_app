import logging
import os
import sys
import time
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
from health_connect_fetch import download_zip_from_drive, extract_db_files, get_credentials
from health_connect_ingest import ingest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / "infrastructure" / ".env"
LOG_DIR = PROJECT_ROOT / "logs"
load_dotenv(ENV_FILE)
FILE_ID = os.getenv("GOOGLE_DRIVE_EXPORT_FILE_ID")


def setup_logging() -> logging.Logger:
    """Configure logging to both console and daily log file."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_file = LOG_DIR / f"ingestion_log_{date.today().strftime('%Y%m%d')}.log"

    logger = logging.getLogger("health_connect_ingestion")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Log to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Log to file
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def main():
    logger = setup_logging()
    start_time = time.time()

    logger.info("========================================")
    logger.info("HEALTH CONNECT INGESTION PIPELINE")
    logger.info("========================================")

    try:
        logger.info("[1/2] Downloading Health Connect export...")

        creds = get_credentials()

        zip_buffer = download_zip_from_drive(
            FILE_ID,
            creds
        )

        db_files = extract_db_files(
            zip_buffer,
            PROJECT_ROOT / "data" / "health_connect"
            )

        logger.info("Successfully downloaded and extracted the following database files:")

        for db_file in db_files:
            logger.info("  - %s", db_file.resolve())

        logger.info("Download and extraction completed in %.2f seconds",time.time() - start_time)
        logger.info("[2/2] Loading database into Bronze...")

        for db_file in db_files:
            logger.info("Ingesting: %s", db_file.name)
            ingest(db_file)

        execution_time = time.time() - start_time

        logger.info("========================================")
        logger.info("PIPELINE SUCCESS")
        logger.info("Total execution time: %.2f seconds", execution_time)
        logger.info("========================================")

    except Exception:
        execution_time = time.time() - start_time

        logger.exception("========================================")
        logger.exception("PIPELINE FAILED")
        logger.exception("Execution time before failure: %.2f seconds", execution_time)
        logger.exception("========================================")

        sys.exit(1)


if __name__ == "__main__":
    main()