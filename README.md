<p align="center">
  <img src="https://raw.githubusercontent.com/Garcez7R/heimdall-gatekeeper/main/logo.png" alt="Heimdall Gatekeeper logo" width="220" />
</p>

# ᚺ Heimdall Gatekeeper

<p align="center">
  <strong>Select language:</strong>
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

Heimdall Gatekeeper is a practical, easy-to-run SIEM demo with a polished dashboard, automated event processing, and threat context. It is designed to be approachable for anyone curious about security operations, while still showing real detection and alerting workflows. No prior security knowledge is required—just run the app and explore the dashboard.

## What this project does for you

- normalized event ingestion from structured inputs
- YAML-based detection rules with severity escalation
- alert lifecycle with acknowledge and resolve flows
- CVE-aware enrichment for vulnerability-linked events
- operational metrics and security-console overview
- local runtime, Docker workflow and Cloudflare deployment path

This is a compact project, but it behaves like a serious security-oriented product rather than a simple CRUD demo.

## Core Capabilities

- FastAPI backend with modular API routes
- SQLite persistence for events, alerts, metrics and rule hits
- Pages Functions + D1 path prepared for Cloudflare deployment
- live dashboard with overview, alerts, events and status views
- automatic demo bootstrap for immediate showcase use
- dark/light theme, density control, high contrast and reduced motion
- multilingual UI: `pt-BR`, `en`, `es`
- CI pipeline with lint, formatting, SAST, dependency audit, tests and Docker build

## Quick Access

### Local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
# requirements-dev.txt includes test and quality tools, but the app runs with requirements.txt alone
cp .env.example .env
uvicorn backend.api.main:app --reload
```

Open:

- `http://127.0.0.1:8000`

### Demo bootstrap

- browser: `http://127.0.0.1:8000/api/demo/bootstrap`
- terminal:

```bash
curl http://127.0.0.1:8000/api/demo/bootstrap
```

### Cloudflare

1. Create D1:

```bash
npx wrangler d1 create heimdall-gatekeeper
```

2. Apply schema:

```bash
npx wrangler d1 execute heimdall-gatekeeper --remote --file=cloudflare/d1/0001_init.sql
```

3. In Pages use:
- Framework preset: `None`
- Build command: empty
- Build output directory: `frontend`

4. Confirm D1 binding:
- Binding name: `DB`

## Full Documentation

- [Português (BR)](./README.pt-BR.md)
- [English](./README.md)
- [Español](./README.es.md)

## Why It Matters in the Portfolio

This project was built to demonstrate practical capability across:

- Blue Team workflow and detection thinking
- SecOps-style event processing
- security product UX and operational dashboards
- Python backend organization with testing and CI
- deployment thinking across local, container and cloud environments

## License

Educational and portfolio use.
