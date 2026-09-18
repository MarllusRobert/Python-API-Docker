from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Python API Docker Demo",
    description="CRUD de clientes em memória — FastAPI + Docker (portfolio)",
    version="1.0.0",
)


class ClienteIn(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    documento: str = ""
    cidade: str = ""
    telefone: str = ""
    email: str = ""


class Cliente(ClienteIn):
    id: int
    created_at: str


_db: dict[int, Cliente] = {}
_seq = 1


def _seed() -> None:
    global _seq
    if _db:
        return
    samples = [
        ClienteIn(nome="Floricultura Encanto", documento="00.111.222/0001-33", cidade="Rio Verde", telefone="64 99999-1001", email="contato@encanto.demo"),
        ClienteIn(nome="Casa Bella Decora", documento="11.222.333/0001-44", cidade="Goiânia", telefone="62 98888-2002", email="compras@casabella.demo"),
    ]
    for s in samples:
        cid = _seq
        _seq += 1
        _db[cid] = Cliente(id=cid, created_at=datetime.utcnow().isoformat() + "Z", **s.model_dump())


@app.on_event("startup")
def on_startup() -> None:
    _seed()


@app.get("/health")
def health():
    return {"status": "ok", "service": "Python-API-Docker"}


@app.get("/api/clientes", response_model=list[Cliente])
def listar():
    return sorted(_db.values(), key=lambda c: c.id, reverse=True)


@app.get("/api/clientes/{cliente_id}", response_model=Cliente)
def obter(cliente_id: int):
    if cliente_id not in _db:
        raise HTTPException(404, "Cliente não encontrado")
    return _db[cliente_id]


@app.post("/api/clientes", response_model=Cliente, status_code=201)
def criar(body: ClienteIn):
    global _seq
    cid = _seq
    _seq += 1
    cliente = Cliente(id=cid, created_at=datetime.utcnow().isoformat() + "Z", **body.model_dump())
    _db[cid] = cliente
    return cliente


@app.put("/api/clientes/{cliente_id}", response_model=Cliente)
def atualizar(cliente_id: int, body: ClienteIn):
    if cliente_id not in _db:
        raise HTTPException(404, "Cliente não encontrado")
    antigo = _db[cliente_id]
    atualizado = Cliente(id=cliente_id, created_at=antigo.created_at, **body.model_dump())
    _db[cliente_id] = atualizado
    return atualizado


@app.delete("/api/clientes/{cliente_id}", status_code=204)
def excluir(cliente_id: int):
    if cliente_id not in _db:
        raise HTTPException(404, "Cliente não encontrado")
    del _db[cliente_id]
    return None


@app.get("/", response_class=HTMLResponse)
def ui():
    return """
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Python API Docker Demo</title>
  <style>
    body{font-family:Segoe UI,sans-serif;margin:0;background:#f4f7f6;color:#15231c}
    header{background:#0f4c57;color:#fff;padding:18px 24px}
    main{max-width:900px;margin:24px auto;padding:0 16px}
    .card{background:#fff;border:1px solid #d7e0db;border-radius:14px;padding:16px;margin-bottom:16px}
    input,button{padding:8px 10px;margin:4px 4px 4px 0;border-radius:8px;border:1px solid #ccd}
    button{background:#2ea08c;color:#fff;border:none;cursor:pointer}
    table{width:100%;border-collapse:collapse}
    th,td{padding:8px;border-bottom:1px solid #eee;text-align:left;font-size:14px}
    a{color:#1f6b57}
  </style>
</head>
<body>
  <header>
    <h1 style="margin:0;font-size:1.3rem">Python API + Docker — Clientes</h1>
    <p style="margin:6px 0 0;opacity:.85">FastAPI · CRUD · /health · portfolio</p>
  </header>
  <main>
    <div class="card">
      <strong>Novo cliente</strong><br/>
      <input id="nome" placeholder="Nome" style="width:220px"/>
      <input id="cidade" placeholder="Cidade" style="width:140px"/>
      <input id="email" placeholder="E-mail" style="width:200px"/>
      <button onclick="criar()">Salvar</button>
    </div>
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <strong>Lista</strong>
        <button onclick="carregar()">Atualizar</button>
      </div>
      <table><thead><tr><th>ID</th><th>Nome</th><th>Cidade</th><th>E-mail</th><th></th></tr></thead>
      <tbody id="tb"></tbody></table>
    </div>
    <p>API: <a href="/docs">/docs</a> · <a href="/health">/health</a> · <a href="/api/clientes">/api/clientes</a></p>
  </main>
  <script>
    async function carregar(){
      const r = await fetch('/api/clientes');
      const data = await r.json();
      tb.innerHTML = data.map(c => `<tr>
        <td>${c.id}</td><td>${c.nome}</td><td>${c.cidade||''}</td><td>${c.email||''}</td>
        <td><button onclick="excluir(${c.id})" style="background:#b45">Excluir</button></td>
      </tr>`).join('');
    }
    async function criar(){
      const body = {nome:nome.value.trim(), cidade:cidade.value.trim(), email:email.value.trim(), documento:'', telefone:''};
      if(!body.nome){ alert('Informe o nome'); return; }
      await fetch('/api/clientes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      nome.value=cidade.value=email.value='';
      carregar();
    }
    async function excluir(id){
      if(!confirm('Excluir?')) return;
      await fetch('/api/clientes/'+id,{method:'DELETE'});
      carregar();
    }
    carregar();
  </script>
</body>
</html>
"""
