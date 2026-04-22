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

Enterprise-style mini-SIEM focused on Blue Team, SecOps and DevSecOps portfolio value. Heimdall Gatekeeper stays intentionally lightweight while still delivering event ingestion, YAML-based detections, alerting, CVE enrichment, operational metrics and a professional dashboard.

## Highlights

- FastAPI backend with modular API routes
- YAML detection rules with regex matching and severity escalation
- SQLite persistence for events, alerts, rule hits and cached CVE intelligence
- D1-ready Cloudflare path via Pages Functions and D1 schema
- Enterprise dashboard with dark/light mode, i18n and accessibility toggles
- Demo bootstrap data for immediate presentation and pilot testing
- Docker, GitHub Actions, Bandit and dependency audit in CI
- Environment-based configuration overrides via `.env`

## Architecture

```text
Log / JSON Event
      |
      v
Normalization -> Rule Engine -> Alert Store -> Overview API -> Web Console
      |                |               |
      |                |               +-> Active alerts / status / metrics
      |                +-> CVE enrichment cache
      +-> SQLite or D1-backed event store
```

## Project Structure

```text
heimdall-gatekeeper/
├── backend/
│   ├── api/
│   ├── core/
│   ├── rules/
│   ├── storage/
│   └── threat_intel/
├── cloudflare/
│   └── d1/
├── config/
├── docker/
├── frontend/
│   ├── css/
│   ├── i18n/
│   └── js/
├── functions/
├── tests/
└── .github/workflows/
```

## Run Locally

### 1. Prepare the environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

### 2. Start the API + dashboard

```bash
uvicorn backend.api.main:app --reload
```

Open:

- `http://127.0.0.1:8000`

The backend serves the frontend directly, so local access is a single URL.

### 3. Bootstrap demo data manually if needed

The app auto-seeds when the database is empty. You can also trigger it manually:

```bash
curl -X POST http://127.0.0.1:8000/api/demo/bootstrap
```

### 4. Example test event

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

## Run with Docker

```bash
docker build -f docker/Dockerfile -t heimdall-gatekeeper .
docker run -p 8000:8000 heimdall-gatekeeper
```

Or:

```bash
docker compose -f docker/docker-compose.yml up --build
```

Then open:

- `http://127.0.0.1:8000`

## Cloudflare Deployment

Heimdall is prepared to run online with:

- `Pages` for the static console
- `Pages Functions` for API routes
- `D1` for storage

### 1. Create the D1 database

```bash
npx wrangler d1 create heimdall-gatekeeper
```

Copy the generated `database_id`.

### 2. Update the binding

Edit [wrangler.toml](/home/rgarcez/Documentos/heimdall-gatekeeper/wrangler.toml) and confirm:

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

### 4. Create the Pages project

In Cloudflare Pages, connect this repository and use:

- Framework preset: `None`
- Build command: leave empty
- Build output directory: `frontend`

### 5. Confirm D1 binding in Pages

In the Pages project settings:

- Functions
- D1 bindings
- Binding name: `DB`
- Database: `heimdall-gatekeeper`

### 6. Deploy and validate

After the first deploy, test:

- `/api/config`
- `/api/overview`
- `/api/demo/bootstrap`

Then open the dashboard URL on `pages.dev`.

## Quality Gates

Run locally:

```bash
pytest
python3 -m compileall backend tests
```

CI currently includes:

- `flake8`
- `black --check`
- `bandit`
- `pip-audit`
- `pytest`
- Docker build

## Roadmap

- authenticated multi-user console
- stronger operator audit trail
- MITRE navigator export
- syslog/file watcher ingestion workers
- richer CVE scoring and enrichment pipeline
- persistent analyst preferences in remote mode

## Why It Matters

This project was built to demonstrate practical skills across:

- Blue Team monitoring
- SecOps event pipelines
- DevSecOps packaging and CI/CD
- security-oriented UX with low operational overhead
- hybrid local/cloud deployment thinking

## License

Educational and portfolio use.
