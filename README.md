<p align="center">
  <img src="./frontend/assets/img/logo.png" alt="Heimdall Gatekeeper logo" width="128" />
</p>

# ᚺ Heimdall Gatekeeper

![Python](https://img.shields.io/badge/Python-3.11%2B-0f172a?style=for-the-badge&logo=python&logoColor=ffd43b)
![FastAPI](https://img.shields.io/badge/FastAPI-Security%20API-0f172a?style=for-the-badge&logo=fastapi&logoColor=22c55e)
![SQLite](https://img.shields.io/badge/SQLite-Lightweight%20Storage-0f172a?style=for-the-badge&logo=sqlite&logoColor=7dd3fc)
![Docker](https://img.shields.io/badge/Docker-Ready-0f172a?style=for-the-badge&logo=docker&logoColor=60a5fa)
![CI](https://img.shields.io/github/actions/workflow/status/Garcez7R/heimdall-gatekeeper/ci.yml?branch=main&style=for-the-badge&label=CI)
![Security](https://img.shields.io/badge/Blue%20Team-SecOps%20Ready-0f172a?style=for-the-badge&logo=shield&logoColor=86efac)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Pages%20%2B%20Functions%20%2B%20D1-0f172a?style=for-the-badge&logo=cloudflare&logoColor=f59e0b)
![i18n](https://img.shields.io/badge/i18n-PT--BR%20%7C%20EN%20%7C%20ES-0f172a?style=for-the-badge&logo=googletranslate&logoColor=93c5fd)
![Accessibility](https://img.shields.io/badge/A11y-High%20Contrast%20%26%20Reduce%20Motion-0f172a?style=for-the-badge&logo=dependabot&logoColor=86efac)

Minimal SIEM built for Blue Team, SecOps and DevSecOps portfolio demonstration. Heimdall Gatekeeper was designed to be lightweight, readable and easy to run, while still showing the core mechanics of a real security console: event ingestion, rule-based detection, alert triage, CVE context, operational metrics and a polished dashboard.

## What This Project Demonstrates

Heimdall Gatekeeper was built as a practical mini-SIEM with emphasis on:

- normalized event ingestion from structured inputs
- YAML-based detection rules with severity escalation
- alert lifecycle handling for acknowledge and resolve flows
- CVE-aware enrichment for vulnerability-linked events
- operational metrics and overview telemetry
- dashboard UX designed for analysts and technical stakeholders
- local runtime, Docker workflow and Cloudflare deployment path

It is intentionally compact, but it already behaves like a serious security-oriented product rather than a simple CRUD demo.

## Core Capabilities

- FastAPI backend with modular API routes
- SQLite persistence for events, alerts, metrics and rule hits
- Pages Functions + D1 path prepared for Cloudflare deployment
- live dashboard with overview, alerts, events and status views
- demo bootstrap for immediate showcase use
- dark/light theme, density control, high contrast and reduced motion
- multilingual UI: `pt-BR`, `en`, `es`
- CI pipeline with lint, formatting, SAST, dependency audit, tests and Docker build

## Architecture

```text
Structured Event
      |
      v
Normalization -> Rule Engine -> Alert Store -> Overview API -> Security Console
      |                |               |
      |                |               +-> live metrics, triage and status
      |                +-> CVE-linked detection context
      +-> SQLite or D1-backed event persistence
```

## Project Structure

```text
heimdall-gatekeeper/
├── backend/
│   ├── api/            # FastAPI entrypoint, routes, schemas and error handling
│   ├── core/           # pipeline, config, metrics, models, seed logic
│   ├── rules/          # YAML detection rules
│   ├── storage/        # SQLite access layer
│   └── threat_intel/   # CVE enrichment helpers
├── cloudflare/
│   └── d1/             # D1 schema for remote mode
├── config/             # app configuration
├── docker/             # container runtime files
├── frontend/           # static dashboard assets
├── functions/          # Cloudflare Pages Functions
├── tests/              # automated tests
└── .github/workflows/  # CI pipeline
```

## Local Access

### 1. Prepare the environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

### 2. Start the application

```bash
uvicorn backend.api.main:app --reload
```

Open:

- `http://127.0.0.1:8000`

The FastAPI application serves both the API and the dashboard, so local access is a single URL.

### 3. Demo mode

The project auto-seeds demo data when the database is empty. You can also trigger the demo bootstrap directly:

- browser: `http://127.0.0.1:8000/api/demo/bootstrap`
- terminal:

```bash
curl http://127.0.0.1:8000/api/demo/bootstrap
```

After that, return to the main page and the dashboard will load with sample events and alerts.

### 4. Ingest a test event manually

```bash
curl -X POST http://127.0.0.1:8000/api/events/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "source":"auth-gateway",
    "event_type":"failed_login",
    "title":"Repeated login failure",
    "message":"Multiple failed login attempts for admin user",
    "severity":"medium",
    "ip_address":"198.51.100.24"
  }'
```

## Docker Access

### Build manually

```bash
docker build -f docker/Dockerfile -t heimdall-gatekeeper .
docker run -p 8000:8000 heimdall-gatekeeper
```

### Or use Docker Compose

```bash
docker compose -f docker/docker-compose.yml up --build
```

Then open:

- `http://127.0.0.1:8000`

## Cloudflare Access

Heimdall Gatekeeper is prepared to run online with:

- `Pages` for the dashboard
- `Pages Functions` for the API layer
- `D1` for remote persistence

### 1. Create the D1 database

```bash
npx wrangler d1 create heimdall-gatekeeper
```

Copy the generated `database_id`.

### 2. Confirm the D1 binding

Check [wrangler.toml](/home/rgarcez/Documentos/heimdall-gatekeeper/wrangler.toml):

```toml
[[d1_databases]]
binding = "DB"
database_name = "heimdall-gatekeeper"
database_id = "YOUR-REAL-D1-ID"
```

### 3. Apply the schema

```bash
npx wrangler d1 execute heimdall-gatekeeper --remote --file=cloudflare/d1/0001_init.sql
```

### 4. Configure Pages

When connecting the repository in Cloudflare Pages, use:

- Framework preset: `None`
- Build command: leave empty
- Build output directory: `frontend`

### 5. Confirm the binding in Pages

Inside the Pages project settings:

- `Functions`
- `D1 bindings`
- Binding name: `DB`
- Database: `heimdall-gatekeeper`

### 6. Validate the online deployment

Test these URLs after deploy:

- `/api/config`
- `/api/overview`
- `/api/demo/bootstrap`

Then open the public `pages.dev` URL for the full console.

## Quality and Validation

Recommended local checks:

```bash
./.venv/bin/pytest
python3 -m compileall backend tests
```

The CI workflow currently runs:

- `flake8`
- `black --check`
- `bandit`
- `pip-audit`
- `pytest`
- Docker build validation

## Why It Matters in the Portfolio

This project was built to show practical capability across:

- Blue Team thinking and detection workflow
- SecOps-style event processing
- security product UX and operational dashboards
- Python backend organization with testing and CI
- deployment thinking across local, container and cloud environments

It is a compact project, but it communicates architecture, security mindset, product design and delivery discipline in one place.

## Roadmap

- authenticated multi-user console
- richer audit trail for analyst actions
- expanded CVE and MITRE context
- ingestion adapters for more event sources
- stronger remote-state synchronization in cloud mode

## License

Educational and portfolio use.
