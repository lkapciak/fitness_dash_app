import io
import os
import zipfile
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / "infrastructure" / ".env"

load_dotenv(ENV_FILE)

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
CREDENTIALS_FILE = "../infrastructure/google_drive_credentials.json"
TOKEN_FILE = "../infrastructure/google_drive_token.json"

FILE_ID = os.getenv("GOOGLE_DRIVE_EXPORT_FILE_ID")
OUTPUT_DIR = Path("../data/health_connect")


def get_credentials() -> Credentials:
    """Returns valid user credentials from storage or initiates an OAuth2 flow."""
    creds = None

    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        Path(TOKEN_FILE).write_text(creds.to_json())

    return creds


def download_zip_from_drive(file_id: str, creds: Credentials) -> io.BytesIO:
    """Downloads a file with a given ID from Google Drive to a memory buffer."""
    service = build("drive", "v3", credentials=creds)
    request = service.files().get_media(fileId=file_id)

    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Downloading: {int(status.progress() * 100)}%")

    buffer.seek(0)
    return buffer


def extract_db_files(zip_buffer: io.BytesIO, output_dir: Path) -> list[Path]:
    """Extracts .db files from a zip archive, stamps them with today's date,
    and returns their paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    extracted = []
    today = date.today().strftime("%Y%m%d")

    with zipfile.ZipFile(zip_buffer) as zf:
        db_members = [n for n in zf.namelist() if n.lower().endswith(".db")]
        if not db_members:
            raise FileNotFoundError("No .db files found in the zip archive.")

        for name in db_members:
            zf.extract(name, output_dir)

            original_path = output_dir / name
            dated_name = f"{original_path.stem}_{today}{original_path.suffix}"
            dated_path = output_dir / dated_name

            original_path.replace(dated_path)
            extracted.append(dated_path)

    return extracted


def main():
    creds = get_credentials()
    zip_buffer = download_zip_from_drive(FILE_ID, creds)
    db_files = extract_db_files(zip_buffer, OUTPUT_DIR)

    for f in db_files:
        print(f"Extracted: {f.resolve()}")

if __name__ == "__main__":
    main()