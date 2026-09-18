@echo off
setlocal
cd /d "%~dp0"

where docker >nul 2>&1
if errorlevel 1 (
  echo Docker nao encontrado. Alternativa local:
  echo   python -m pip install -r requirements.txt
  echo   python -m uvicorn app.main:app --reload --port 8080
  exit /b 1
)

echo Subindo API com Docker Compose...
docker compose up --build -d
if errorlevel 1 exit /b 1

echo.
echo API:     http://127.0.0.1:8080
echo Docs:    http://127.0.0.1:8080/docs
echo Health:  http://127.0.0.1:8080/health
start "" http://127.0.0.1:8080
endlocal
