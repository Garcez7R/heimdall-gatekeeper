# ᚺ Heimdall Gatekeeper

![Python](https://img.shields.io/badge/Python-3.11%2B-0f172a?style=for-the-badge&logo=python&logoColor=ffd43b)
![FastAPI](https://img.shields.io/badge/FastAPI-Security%20API-0f172a?style=for-the-badge&logo=fastapi&logoColor=22c55e)
![SQLite](https://img.shields.io/badge/SQLite-Lightweight%20Storage-0f172a?style=for-the-badge&logo=sqlite&logoColor=7dd3fc)
![Docker](https://img.shields.io/badge/Docker-Ready-0f172a?style=for-the-badge&logo=docker&logoColor=60a5fa)
![CI](https://img.shields.io/github/actions/workflow/status/Garcez7R/heimdall-gatekeeper/ci.yml?branch=main&style=for-the-badge&label=CI)
![Security](https://img.shields.io/badge/Blue%20Team-SecOps%20Ready-0f172a?style=for-the-badge&logo=shield&logoColor=86efac)
![Cloudflare](https://img.shields.io/badge/Cloudflare-D1%20Roadmap-0f172a?style=for-the-badge&logo=cloudflare&logoColor=f59e0b)

Enterprise-style mini-SIEM focused on Blue Team, SecOps and DevSecOps portfolio value. Heimdall Gatekeeper was designed to stay lightweight while still delivering event ingestion, YAML-based detections, alerting, CVE enrichment, operational metrics and a professional dashboard.

## Highlights

- FastAPI backend with lightweight JSON APIs
- YAML detection rules with regex matching and severity
- SQLite persistence for events, alerts, rule hits and cached CVE intelligence
- NVD CVE enrichment with local cache
- Enterprise dashboard with dark/light mode, i18n and accessibility toggles
- Docker, GitHub Actions and security scanning pipeline
- Cloudflare D1-ready architecture for future sync mode

## Architecture

```text
Log / JSON Event
      |
      v
Normalization -> Rule Engine -> Alert Store -> Dashboard API -> Web Console
      |                |               |
      |                |               +-> Active alerts / status / metrics
      |                +-> CVE enrichment cache
      +-> SQLite event store
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
├── frontend/
│   ├── css/
│   ├── i18n/
│   └── js/
├── config/
├── docker/
├── tests/
└── .github/workflows/
```

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn backend.api.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Docker

```bash
docker build -f docker/Dockerfile -t heimdall-gatekeeper .
docker run -p 8000:8000 heimdall-gatekeeper
```

Or:

```bash
docker compose -f docker/docker-compose.yml up --build
```

## Example Test Event

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

## Roadmap

- Cloudflare D1 sync mode
- Alert cooldown persistence
- MITRE navigator export
- Syslog/file watcher ingestion workers
- Authenticated multi-user console
- Charts and timeline expansion

## Why It Matters

This project was built to demonstrate practical skills across:

- Blue Team monitoring
- SecOps event pipelines
- DevSecOps packaging and CI/CD
- Security-oriented UX with low operational overhead

## License

Educational and portfolio use.
