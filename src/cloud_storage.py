import logging
from abc import ABC, abstractmethod
from pathlib import Path

logger = logging.getLogger(__name__)


class CloudStorage(ABC):
    #Contrato: qualquer nuvem (S3, Drive...) precisa implementar upload().

    @abstractmethod
    def upload(self, arquivo: Path) -> bool:
        ...


class S3Storage(CloudStorage):
    #Envia arquivos para um bucket AWS S3.

    def __init__(self, bucket, access_key, secret_key, region, client=None):
        self.bucket = bucket
        if client is None:
            import boto3  # import aqui, testes não precisam do boto3 instalado
            client = boto3.client(
                "s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
            )
        self.client = client

    def upload(self, arquivo: Path) -> bool:
        try:
            self.client.upload_file(str(arquivo), self.bucket, f"backups/{arquivo.name}")
            logger.info("Enviado ao S3: %s", arquivo.name)
            return True
        except Exception as e:
            logger.error("Falha no upload: %s", e)
            return False


import shutil


class LocalStorage(CloudStorage):
    #Nuvem simulada: copia o zip pra uma pasta local (pra testar sem AWS).

    def __init__(self, destino):
        self.destino = Path(destino)
        self.destino.mkdir(parents=True, exist_ok=True)

    def upload(self, arquivo: Path) -> bool:
        try:
            shutil.copy2(arquivo, self.destino / arquivo.name)
            logger.info("Enviado (simulado) para: %s", self.destino)
            return True
        except Exception as e:
            logger.error("Falha no upload simulado: %s", e)
            return False


class CloudRestore(ABC):
    #Contrato: qualquer nuvem precisa saber baixar um arquivo de volta.

    @abstractmethod
    def download(self, object_key: str, destino: Path) -> bool:
        ...


class S3Restore(CloudRestore):
    #Baixa arquivos do S3 — usa um usuário só de leitura, separado do backup-script.

    def __init__(self, bucket, access_key, secret_key, region, client=None):
        self.bucket = bucket
        if client is None:
            import boto3
            client = boto3.client(
                "s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
            )
        self.client = client

    def download(self, object_key: str, destino: Path) -> bool:
        try:
            self.client.download_file(self.bucket, object_key, str(destino))
            logger.info("Restaurado do S3: %s -> %s", object_key, destino)
            return True
        except Exception as e:
            logger.error("Falha na restauração: %s", e)
            return False