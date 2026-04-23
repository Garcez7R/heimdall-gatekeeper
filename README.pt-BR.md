<p align="center">
  <img src="./frontend/assets/img/logo.png" alt="Logotipo do Heimdall Gatekeeper" width="128" />
</p>

# ᚺ Heimdall Gatekeeper

<p align="center">
  <strong>Selecionar idioma:</strong>
  <a href="./README.pt-BR.md">Português (BR)</a> |
  <a href="./README.md">English</a> |
  <a href="./README.es.md">Español</a>
</p>

![Python](https://img.shields.io/badge/Python-3.11%2B-0f172a?style=for-the-badge&logo=python&logoColor=ffd43b)
![FastAPI](https://img.shields.io/badge/FastAPI-Security%20API-0f172a?style=for-the-badge&logo=fastapi&logoColor=22c55e)
![SQLite](https://img.shields.io/badge/SQLite-Lightweight%20Storage-0f172a?style=for-the-badge&logo=sqlite&logoColor=7dd3fc)
![Docker](https://img.shields.io/badge/Docker-Ready-0f172a?style=for-the-badge&logo=docker&logoColor=60a5fa)
![CI](https://img.shields.io/github/actions/workflow/status/Garcez7R/heimdall-gatekeeper/ci.yml?branch=main&style=for-the-badge&label=CI)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Pages%20%2B%20Functions%20%2B%20D1-0f172a?style=for-the-badge&logo=cloudflare&logoColor=f59e0b)

Mini-SIEM criado para demonstração de portfólio em Blue Team, SecOps e DevSecOps. O Heimdall Gatekeeper foi pensado para ser leve, fácil de executar e visualmente forte, sem abrir mão de mecanismos centrais de um console de segurança real: ingestão de eventos, detecção por regras, triagem de alertas, contexto de CVE e visibilidade operacional.

## O Que Este Projeto Demonstra

- ingestão normalizada de eventos estruturados
- regras YAML com escalonamento de severidade
- ciclo de vida de alertas com reconhecimento e resolução
- enriquecimento com contexto de vulnerabilidades vinculadas a CVEs
- métricas operacionais e visão geral de console de segurança
- execução local, via Docker e com caminho pronto para Cloudflare

É um projeto compacto, mas já se comporta como um produto orientado à segurança, e não como um CRUD simples.

## Capacidades Principais

- backend FastAPI com rotas modulares
- persistência em SQLite para eventos, alertas, métricas e rule hits
- caminho preparado para Cloudflare com Pages Functions + D1
- dashboard vivo com visão geral, alertas, eventos e status
- bootstrap automático de dados demo para apresentação imediata
- tema dark/light, ajuste de densidade, alto contraste e redução de movimento
- interface multilíngue: `pt-BR`, `en`, `es`
- pipeline de CI com lint, formatação, SAST, auditoria de dependências, testes e build Docker

## Acesso Rápido

### Local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
uvicorn backend.api.main:app --reload
```

Abra:

- `http://127.0.0.1:8000`

### Bootstrap demo

- navegador: `http://127.0.0.1:8000/api/demo/bootstrap`
- terminal:

```bash
curl http://127.0.0.1:8000/api/demo/bootstrap
```

### Cloudflare

1. Criar o D1:

```bash
npx wrangler d1 create heimdall-gatekeeper
```

2. Aplicar o schema:

```bash
npx wrangler d1 execute heimdall-gatekeeper --remote --file=cloudflare/d1/0001_init.sql
```

3. No Pages usar:
- Framework preset: `None`
- Build command: vazio
- Build output directory: `frontend`

4. Confirmar binding D1:
- Binding name: `DB`

## Documentação Completa

- [Português (BR)](./README.pt-BR.md)
- [English](./README.md)
- [Español](./README.es.md)

## Por Que Ele Importa no Portfólio

Este projeto foi construído para demonstrar capacidade prática em:

- fluxo de trabalho e pensamento Blue Team
- processamento de eventos no estilo SecOps
- UX de produto de segurança e dashboards operacionais
- organização de backend Python com testes e CI
- pensamento de deploy em ambiente local, container e nuvem

## Licença

Uso educacional e de portfólio.
