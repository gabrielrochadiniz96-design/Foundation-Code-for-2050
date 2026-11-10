import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BackupCleaner:
    #Mantém só os 5 backups locais mais recentes.

    def __init__(self, pasta, manter=5):
        self.pasta = Path(pasta)
        self.manter = manter

    def limpar(self):
        zips = sorted(self.pasta.glob("backup_*.zip"), key=lambda p: p.stat().st_mtime)
        excedentes = zips[:-self.manter] if self.manter > 0 else zips
        for velho in excedentes:
            velho.unlink()
            logger.info("Este backup antigo foi removido: %s", velho.name)


class BackupJob:
    #Orquestra: compactar - enviar pra nuvem - limpar antigos.

    def __init__(self, compressor, storage, cleaner):
        self.compressor = compressor
        self.storage = storage
        self.cleaner = cleaner

    def run(self) -> bool:
        logger.info("=== Inícializando o backup ===")
        try:
            zip_path = self.compressor.compress()
            enviado = self.storage.upload(zip_path)
            if enviado:
                self.cleaner.limpar()
            else:
                logger.warning("Upload falhou: backup local mantido em %s", zip_path)
            logger.info("=== Backup finalizado ===")
            return enviado
        except Exception as e:
            logger.error("Falha no Backup: %s", e)
            return False
