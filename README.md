# FinLab API

## Como Executar a API

1. Ative o ambiente virtual e entre no diretório `api`:
```bash
source .venv/bin/activate
cd api
```

2. Inicie o servidor localmente com o Uvicorn:
```bash
uv run uvicorn main:app --reload
```
A API estará disponível em `http://127.0.0.1:8000`.

A documentação interativa (Swagger) pode ser acessada em `http://127.0.0.1:8000/docs`.

## Exemplos de Uso

Abaixo estão alguns exemplos de requisições `curl` para os endpoints da API.

### Endpoint `/rag`

Endpoint para gerar uma resposta com base no contexto recuperado.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/rag' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "what are Apple'\''s main financial risks?",
  "limit": 3
}'
```

### Endpoint `/search`

Endpoint para buscar documentos e contextos na base de dados (Qdrant).

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/search' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "what are Apple'\''s main financial risks?",
  "limit": 3
}'
```
