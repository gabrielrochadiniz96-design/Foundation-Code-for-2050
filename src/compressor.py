import logging
import zipfile
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class BackupCompressor:
    #Compacta uma pasta inteira em um .zip com data/hora no nome.

    def __init__(self, source_dir, output_dir):
        self.source = Path(source_dir)
        self.output = Path(output_dir)
        self.output.mkdir(parents=True, exist_ok=True)

    def compress(self) -> Path:
        if not self.source.exists():
            raise FileNotFoundError(f"Pasta de origem não existente: {self.source}")

        nome = f"backup_{datetime.now():%Y%m%d_%H%M%S}.zip"
        destino = self.output / nome

        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zf:
            for arquivo in self.source.rglob("*"):
                if arquivo.is_file():
                    zf.write(arquivo, arquivo.relative_to(self.source))

        logger.info("Compactado: %s (%d bytes)", destino.name, destino.stat().st_size)
        return destino
