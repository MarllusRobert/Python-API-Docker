@echo off
setlocal
cd /d "%~dp0"
title Python-API-Docker

echo.
echo === Python API Docker Demo ===
echo.

REM 1) Tenta Docker se o daemon estiver de pe
where docker >nul 2>&1
if not errorlevel 1 (
  docker info >nul 2>&1
  if not errorlevel 1 (
    echo Docker OK. Subindo com Compose...
    docker compose up --build -d
    if errorlevel 1 (
      echo.
      echo Falhou o Docker Compose. Tentando modo local...
      goto LOCAL
    )
    echo.
    echo API:     http://127.0.0.1:8080
    echo Docs:    http://127.0.0.1:8080/docs
    echo Health:  http://127.0.0.1:8080/health
    start "" http://127.0.0.1:8080
    echo.
    pause
    exit /b 0
  ) else (
    echo Docker instalado, mas o Docker Desktop NAO esta rodando.
    echo Abrindo Docker Desktop... 
    start "" "C:\Users\Marllus Soft\AppData\Local\Programs\DockerDesktop\Docker Desktop.exe" 2>nul
    echo Continuando em modo LOCAL (Python) enquanto o Docker sobe.
    echo.
  )
) else (
  echo Docker nao encontrado no PATH. Usando modo LOCAL (Python).
  echo.
)

:LOCAL
where python >nul 2>&1
if errorlevel 1 (
  echo ERRO: Python nao encontrado no PATH.
  pause
  exit /b 1
)

echo Instalando dependencias...
python -m pip install -r requirements.txt -q
if errorlevel 1 (
  echo Falha ao instalar requirements.
  pause
  exit /b 1
)

echo.
echo Subindo API local em http://127.0.0.1:8080
echo Docs: http://127.0.0.1:8080/docs
echo.
start "" http://127.0.0.1:8080
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080
echo.
echo API encerrada.
pause
endlocal
