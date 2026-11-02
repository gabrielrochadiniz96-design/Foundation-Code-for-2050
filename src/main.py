import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import settings
from src.backup import BackupCleaner, BackupJob
from src.cloud_storage import LocalStorage, S3Storage
from src.compressor import BackupCompressor


def criar_storage():
    if os.getenv("STORAGE", "s3").lower() == "local":
        return LocalStorage(settings.BASE_DIR / "nuvem_simulada")
    return S3Storage(
        settings.S3_BUCKET,
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.AWS_REGION,
    )


def main() -> int:
    settings.setup_logging()

    job = BackupJob(
        compressor=BackupCompressor(settings.SOURCE_DIR, settings.BACKUP_DIR),
        storage=criar_storage(),
        cleaner=BackupCleaner(settings.BACKUP_DIR, settings.KEEP_BACKUPS),
    )
    return 0 if job.run() else 1


if __name__ == "__main__":
    sys.exit(main())
