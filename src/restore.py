import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import settings
from src.cloud_storage import S3Restore


def main() -> int:
    settings.setup_logging()

    if len(sys.argv) < 2:
        print("Uso: python -m src.restore <nome_do_arquivo.zip>")
        print("Exemplo: python -m src.restore backup_20261105_022020.zip")
        return 1

    nome_arquivo = sys.argv[1]
    object_key = f"backups/{nome_arquivo}"
    destino = settings.BASE_DIR / "restaurado" / nome_arquivo
    destino.parent.mkdir(exist_ok=True)

    restore = S3Restore(
        settings.S3_BUCKET,
        settings.AWS_RESTORE_ACCESS_KEY_ID,
        settings.AWS_RESTORE_SECRET_ACCESS_KEY,
        settings.AWS_REGION,
    )

    if restore.download(object_key, destino):
        print(f"Restaurado com sucesso em: {destino}")
        return 0
    print("Falha na restauração. Veja logs/backup.log, para investigar a causa")
    return 1


if __name__ == "__main__":
    sys.exit(main())