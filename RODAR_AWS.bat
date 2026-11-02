@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY="C:\Users\Pichau\AppData\Local\Programs\Python\Python314\python.exe"

if not exist ".env" (
  echo.
  echo  ERRO: nao achei o arquivo .env nesta pasta.
  echo  Copie o arquivo .env.example, renomeie para .env
  echo  e preencha com as chaves da AWS e o nome do bucket.
  echo.
  pause
  exit /b 1
)

echo Instalando dependencias (so demora na 1a vez)...
%PY% -m pip install -r requirements.txt -q

echo.
echo ==============================================
echo  BACKUP REAL - enviando para a AWS S3
echo ==============================================
%PY% -m src.main

echo.
echo  Terminou. Veja o resultado em: logs\backup.log
pause
