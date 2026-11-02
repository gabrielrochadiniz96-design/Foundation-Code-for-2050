import zipfile
from pathlib import Path

from src.backup import BackupCleaner, BackupJob
from src.cloud_storage import CloudStorage
from src.compressor import BackupCompressor


class FakeStorage(CloudStorage):
    def __init__(self, ok=True):
        self.ok = ok
        self.enviados = []

    def upload(self, arquivo: Path) -> bool:
        if self.ok:
            self.enviados.append(arquivo.name)
        return self.ok


def _origem(tmp_path):
    origem = tmp_path / "site"
    (origem / "sub").mkdir(parents=True)
    (origem / "index.html").write_text("oi")
    (origem / "sub" / "a.txt").write_text("a")
    return origem


def test_compressor_gera_zip(tmp_path):
    zip_path = BackupCompressor(_origem(tmp_path), tmp_path / "out").compress()
    with zipfile.ZipFile(zip_path) as zf:
        assert sorted(n.replace("\\", "/") for n in zf.namelist()) == ["index.html", "sub/a.txt"]


def test_cleaner_mantem_so_os_recentes(tmp_path):
    for i in range(1, 6):
        (tmp_path / f"backup_2026110{i}_000000.zip").write_text("x")
    BackupCleaner(tmp_path, manter=2).limpar()
    assert len(list(tmp_path.glob("backup_*.zip"))) == 2


def test_job_sucesso(tmp_path):
    storage = FakeStorage(ok=True)
    out = tmp_path / "out"
    job = BackupJob(BackupCompressor(_origem(tmp_path), out), storage, BackupCleaner(out, 5))
    assert job.run() is True
    assert len(storage.enviados) == 1


def test_job_upload_falha_mantem_backup_local(tmp_path):
    out = tmp_path / "out"
    job = BackupJob(BackupCompressor(_origem(tmp_path), out), FakeStorage(ok=False), BackupCleaner(out, 0))
    assert job.run() is False
    assert len(list(out.glob("backup_*.zip"))) == 1


def test_job_pasta_inexistente(tmp_path):
    out = tmp_path / "out"
    job = BackupJob(BackupCompressor(tmp_path / "nao_existe", out), FakeStorage(), BackupCleaner(out))
    assert job.run() is False
