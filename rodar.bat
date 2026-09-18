@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Python-API-Docker
color 0A

echo.
echo ============================================
echo   Python API Docker Demo
echo ============================================
echo Pasta: %CD%
echo.

REM --- Acha Python REAL (evita stub da Microsoft Store) ---
set "PY="
if exist "%LocalAppData%\Python\bin\python.exe" set "PY=%LocalAppData%\Python\bin\python.exe"
if not defined PY if exist "%LocalAppData%\Programs\Python\Python314\python.exe" set "PY=%LocalAppData%\Programs\Python\Python314\python.exe"
if not defined PY if exist "%LocalAppData%\Programs\Python\Python313\python.exe" set "PY=%LocalAppData%\Programs\Python\Python313\python.exe"
if not defined PY if exist "%LocalAppData%\Programs\Python\Python312\python.exe" set "PY=%LocalAppData%\Programs\Python\Python312\python.exe"
if not defined PY (
  where py >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
  echo ERRO: Python real nao encontrado.
  echo Instale em https://www.python.org/downloads/
  echo.
  pause
  exit /b 1
)

echo Usando Python: %PY%
"%PY%" -c "import sys; print(sys.version)" 2>nul
if errorlevel 1 (
  echo ERRO ao executar Python.
  pause
  exit /b 1
)
echo.

REM --- Docker so se daemon estiver ativo ---
set "USE_DOCKER=0"
where docker >nul 2>&1
if not errorlevel 1 (
  docker info >nul 2>&1
  if not errorlevel 1 set "USE_DOCKER=1"
)

if "%USE_DOCKER%"=="1" (
  echo Docker Desktop ativo. Subindo Compose...
  docker compose up --build -d
  if errorlevel 1 (
    echo Compose falhou. Indo para modo local...
    goto LOCAL
  )
  echo.
  echo API:    http://127.0.0.1:8080
  echo Docs:   http://127.0.0.1:8080/docs
  echo Health: http://127.0.0.1:8080/health
  timeout /t 2 /nobreak >nul
  start "" http://127.0.0.1:8080
  echo.
  echo Container no ar. Pode fechar esta janela.
  pause
  exit /b 0
)

echo Docker Desktop nao esta rodando. Usando modo LOCAL.
echo ^(Nao precisa de Docker para o demo.^)
echo.

:LOCAL
echo Instalando dependencias (pode demorar na 1a vez)...
"%PY%" -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo ERRO no pip. Veja a mensagem acima.
  pause
  exit /b 1
)

echo.
echo ============================================
echo   Subindo API em http://127.0.0.1:8080
echo   Docs: http://127.0.0.1:8080/docs
echo   Deixe esta janela ABERTA.
echo ============================================
echo.

REM abre o browser um pouco depois, em paralelo
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:8080"

"%PY%" -m uvicorn app.main:app --host 127.0.0.1 --port 8080
set "ERR=%ERRORLEVEL%"

echo.
if not "%ERR%"=="0" (
  echo API encerrou com erro %ERR%.
) else (
  echo API encerrada.
)
pause
endlocal
exit /b %ERR%
