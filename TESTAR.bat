@echo off
chcp 65001 >nul
cd /d "%~dp0"
set STORAGE=local
set KEEP_BACKUPS=2
set SOURCE_DIR=%~dp0src
set PY="C:\Users\Pichau\AppData\Local\Programs\Python\Python314\python.exe"

echo ==============================================
echo  TESTE DO BACKUP - vai rodar 4 vezes
echo ==============================================
for /L %%i in (1,1,4) do (
  echo.
  echo --- Rodada %%i de 4 ---
  %PY% -m src.main
  timeout /t 2 >nul
)
echo.
echo ==============================================
echo  PRONTO! Vou abrir as 2 pastas pra voce ver:
echo  - nuvem_simulada: tem os 4 zips (a "nuvem")
echo  - backup: so os 2 mais novos (limpeza funcionou)
echo ==============================================
explorer "%~dp0nuvem_simulada"
explorer "%~dp0backup"
pause
