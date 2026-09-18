# Python API + Docker

Demo **FastAPI** com CRUD de clientes, UI simples e container Docker.

## O que faz

- API REST: GET/POST/PUT/DELETE `/api/clientes`
- `/health` e documentação Swagger em `/docs`
- UI web em `/`
- Seed com 2 clientes
- `Dockerfile` + `docker compose`

## Como rodar

### Docker (recomendado)
```bat
rodar.bat
```
Abre http://127.0.0.1:8080

### Local sem Docker
```bat
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8080
```

## Stack

Python · FastAPI · Uvicorn · Pydantic · Docker

## Para entrevista

- API REST com validação
- Containerização (Dockerfile / Compose)
- Healthcheck e docs OpenAPI
- Complementa portfolio backend Python
