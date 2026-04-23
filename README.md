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

## 📋 Implementation Roadmap

See [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md) for the complete **3-phase deployment plan**:

- **Phase 1** ✅: D1 Persistence, Strict Validation, Rate Limiting & API Keys
- **Phase 2** ✅: Webhooks (Discord/Slack), MITRE ATT&CK Mapping, Advanced Charts  
- **Phase 3** 🚀: Behavioral Correlation, ECS Normalization, Sigma Rules, JWT Auth

This roadmap demonstrates enterprise-grade SIEM evolution from prototype to production-ready.

## Core Capabilities

- FastAPI backend with modular API routes
- SQLite persistence for events, alerts, metrics and rule hits
- Pages Functions + D1 path prepared for Cloudflare deployment
- live dashboard with overview, alerts, events and status views
- enterprise-style alert and event pages with summary cards, severity filters and source breakdown
- automatic demo bootstrap for immediate showcase use
- dark/light theme, density control, high contrast and reduced motion
- multilingual UI: `pt-BR`, `en`, `es`
- CI pipeline with lint, formatting, SAST, dependency audit, tests and Docker build

## Enterprise-ready enhancements

These improvements move the project beyond a basic demo toward a polished security console:

- robust alert filters for status and severity
- event search, severity filtering and source selection
- top-line summary cards for alert and event views
- interactive Chart.js visualizations for event flow and threat sources
- clean enterprise dashboard presentation for analysts and SOC operators

## Technical Architecture

**Detection & Events:**
- YAML-based detection rules with regex pattern matching
- SQLite-backed alert lifecycle management
- Real-time CVE enrichment via NVD integration
- Multi-field event normalization for standard ingestion

**Frontend:**
- Vanilla JavaScript with no build step
- Enterprise dark/light theme with accessibility controls
- Responsive dashboard with independent sidebar and content scrolling
- Internationalization support (pt-BR, en, es)

**Backend:**
- FastAPI with modular route organization
- Pydantic schemas for payload validation
- Automated demo bootstrap for showcase mode
- CI/CD pipeline with linting, formatting, SAST, and Docker builds

## Advanced Roadmap (3-month planning)

### Phase 1: Core Persistence & Stability
- **D1 Integration**: Move from in-memory demo to persistent Cloudflare D1 storage
- **Payload Validation**: Enhance Pydantic schemas to catch malformed event data early
- **Rate Limiting**: Protect ingest endpoints from DoS attacks via IP-based throttling
- **Current Status**: ✅ Backend API ready, D1 schema prepared in `cloudflare/d1/0001_init.sql`

### Phase 2: Advanced Visualizations & UX
- **Chart.js Enhancements**: Timeline graphs for event flow, threat source composition (✅ Added)
- **Custom Alerts**: Real-time Slack/Discord webhook integration for critical detections
- **Alert Deduplication**: Reduce noise by grouping correlated alerts
- **MITRE ATT&CK Mapping**: Visually tag detections with MITRE tactics and techniques

### Phase 3: Production Hardening
- **Sigma Rule Support**: Parse industry-standard Sigma rules into Heimdall format
- **ECS Normalization**: Adopt Elastic Common Schema for field consistency
- **Behavioral Detection**: Multi-stage correlation (e.g., N failed logins → 1 success in T minutes)
- **JWT Authentication**: Secure dashboard with Cloudflare Access or custom token validation
- **KV Cache Layer**: Use Cloudflare KV for fast threat intel lookups during ingestion
- **Queue Processing**: Async event processing via Cloudflare Queues for high-volume environments

## Why This Project Validates Blue Team Competencies

This project demonstrates advanced security engineering beyond "tool usage":

| Competency | Evidence |
|---|---|
| **Log Analysis** | Custom YAML rules, field extraction, severity scoring |
| **Detection Engineering** | Regex patterns, multi-source correlation, alert tuning |
| **Threat Intelligence** | CVE enrichment, IP reputation tracking, MITRE mapping |
| **Incident Response** | Alert triage, acknowledge/resolve workflows, prioritization |
| **Infrastructure as Code** | Docker, GitHub Actions, SQLite schema versioning |
| **Modern Security** | Detection as Code (YAML), DevSecOps automation, event normalization |

## For Blue Team Interviewers

If asked about this project, frame it as:

> "I built Heimdall Gatekeeper to understand the full pipeline of a SIEM—from event ingestion to detection to alerting. I implemented detection rules in YAML, created a schema for normalized events, and integrated threat intelligence enrichment. This gave me hands-on experience in log correlation, false positive tuning, and incident response workflow automation—skills critical for SOC engineering."

## Future roadmap

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

## License

All rights reserved. Unauthorized use, modification, copying, or distribution is prohibited.