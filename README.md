# Foundation Code for 2050
**FOUNDATION 2050 – Smart Home Infrastructure & Security (ExpoTech 2026.2)**

Automação em Python (OOP + pensamento algorítmico) para o servidor doméstico:
compacta uma pasta, envia o `.zip` para a nuvem (AWS S3) e remove backups locais antigos.
Roda na VM configurada pela equipe de infraestrutura e gera logs para monitoramento.

## Fluxo
Compactar -> Enviar ao S3 -> (se enviou) limpar backups locais antigos -> registrar tudo em `logs/backup.log`

## Estrutura
- `config/settings.py` – configurações e log
- `src/compressor.py` – `BackupCompressor` (compacta)
- `src/cloud_storage.py` – `CloudStorage` (abstrata), `S3Storage` (AWS) e `LocalStorage` (nuvem simulada p/ testes)
- `src/backup.py` – `BackupCleaner` e `BackupJob`
- `src/main.py` – ponto de entrada
- `tests/` – testes com pytest

## Como usar
**Teste sem nuvem:** dois cliques em `TESTAR.bat`

**Backup real na AWS:**
1. Copie `.env.example` para `.env` e preencha (o `.env` nunca vai pro Git)
2. Dois cliques em `RODAR_AWS.bat`

**Pelo terminal (na raiz do projeto):** `python -m src.main`
**Testes automáticos:** `python -m pytest`

## Segurança
- Credenciais só no `.env` (ignorado pelo Git)
- Usuário IAM com permissão mínima (somente enviar para `backups/`)
- Bucket com acesso público bloqueado

## Agendamento na VM (Windows Task Scheduler)
- Program: `python` | Arguments: `-m src.main` | Start in: pasta do projeto
- Logs em `logs/backup.log` (monitoramento da equipe de Cyber/Infra)

## Conceitos de POO aplicados
Abstração (`CloudStorage`), herança (`S3Storage`, `LocalStorage`), polimorfismo (`BackupJob` não sabe qual nuvem usa), encapsulamento (uma responsabilidade por classe).
