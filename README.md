<p align="center">
  <img src="https://raw.githubusercontent.com/Garcez7R/heimdall-gatekeeper/main/frontend/assets/img/logo.png" alt="Heimdall Gatekeeper logo" width="220" />
</p>

# ᚺ Heimdall Gatekeeper

<p align="center">
  <strong>Select language:</strong>
  <a href="./README.pt-BR.md">Português (BR)</a> |
  <a href="./README.md">English</a> |
  <a href="./README.es.md">Español</a>
</p>

![Python](https://img.shields.io/badge/Python-3.11%2B-0f172a?style=for-the-badge&logo=python&logoColor=ffd43b)
![FastAPI](https://img.shields.io/badge/FastAPI-Enterprise%20API-0f172a?style=for-the-badge&logo=fastapi&logoColor=22c55e)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Pages%20%2B%20Functions%20%2B%20D1-0f172a?style=for-the-badge&logo=cloudflare&logoColor=f59e0b)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-0f172a?style=for-the-badge&logo=websocket&logoColor=8b5cf6)
![JWT](https://img.shields.io/badge/JWT-Authentication-0f172a?style=for-the-badge&logo=jsonwebtokens&logoColor=ef4444)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-0f172a?style=for-the-badge&logo=chartdotjs&logoColor=10b981)

**Enterprise-Grade SIEM** with real-time dashboards, behavioral detection, and production deployment. Built for SOC teams who need a professional security operations console.

## 🎯 What Makes This Different

Heimdall Gatekeeper is not just another SIEM demo—it's a **production-ready security platform** that demonstrates enterprise-grade capabilities:

- **Real-time WebSocket updates** for live threat monitoring
- **JWT authentication** with role-based access control
- **Async webhook delivery** with retry logic and multi-platform support
- **Behavioral correlation** for advanced threat detection
- **Cloudflare D1 persistence** with automated migrations
- **Comprehensive testing** with 25+ automated test cases
- **OpenAPI documentation** and enterprise UX

## 🚀 Core Capabilities

### 🔐 Security Operations
- **Event Ingestion**: Normalized event processing with ECS field mapping
- **Detection Engine**: YAML-based rules with MITRE ATT&CK tagging
- **Alert Management**: Lifecycle management with acknowledge/resolve workflows
- **Threat Intelligence**: Real-time CVE enrichment via NVD API
- **Behavioral Detection**: Multi-stage correlation patterns

### 📊 Analytics & Visualization
- **Real-time Dashboard**: WebSocket-powered live updates
- **Interactive Charts**: Timeline analysis and threat source visualization
- **Summary Cards**: Aggregated metrics for alerts and events
- **Advanced Filters**: Severity, status, source, and search capabilities

### ☁️ Cloud-Native Architecture
- **Cloudflare Pages**: Frontend deployment with global CDN
- **Cloudflare Functions**: Serverless API backend
- **Cloudflare D1**: Distributed SQLite database
- **Rate Limiting**: Built-in DDoS protection
- **CORS Security**: Cross-origin request protection

### 🧪 Quality Assurance
- **25+ Test Cases**: Comprehensive pytest coverage
- **OpenAPI Docs**: Interactive API documentation
- **CI/CD Pipeline**: Automated testing and deployment
- **Structured Logging**: JSON-formatted audit trails

## 📋 Implementation Status

### ✅ **PHASE 1: Core Persistence & Stability** (COMPLETED)
- **D1 Integration**: Persistent Cloudflare D1 storage
- **Payload Validation**: Enhanced Pydantic schemas with regex patterns
- **Rate Limiting**: 600 requests/hour with proper Retry-After headers
- **API Key Auth**: X-Heimdall-Key header validation

### ✅ **PHASE 2: Advanced UX & Integration** (COMPLETED)
- **Chart.js Visualizations**: Timeline and threat source analytics
- **Webhook Integration**: Discord/Slack notifications with platform-specific formatting
- **MITRE ATT&CK Mapping**: Tactic/technique tagging on alerts and events
- **Enterprise UI**: Dark theme, independent scrolling, summary cards

### ✅ **PHASE 3: Production Hardening** (COMPLETED)
- **JWT Authentication**: Role-based access (admin/analyst) with token expiration
- **Behavioral Correlation**: Multi-stage pattern detection with time windows
- **ECS Normalization**: Elastic Common Schema field mapping
- **Async Processing**: Webhook queue with exponential backoff retry
- **Session Management**: Persistent user sessions with audit logging

### ✅ **PHASE A: Enterprise UX Refinements** (COMPLETED)
- **Real-time Updates**: WebSocket broadcasting for live alerts/events
- **Login System**: Enterprise modal with localStorage persistence
- **Structured Logging**: JSON-formatted request/response tracking
- **Admin Controls**: JWT-protected webhook and system management

### ✅ **PHASE C: Testing & Documentation** (COMPLETED)
- **Comprehensive Tests**: 25+ pytest cases covering all endpoints
- **OpenAPI/Swagger**: Interactive API documentation at `/docs`
- **Performance Testing**: Rate limiting and load validation
- **Production Checks**: CORS, static assets, error handling

### ✅ **PHASE B: Cloud Migration** (COMPLETED)
- **D1 Migrations**: Automated schema updates for all tables
- **Deployment Scripts**: One-click deploy to Cloudflare
- **Production Config**: Environment variables and security headers
- **Testing Suite**: Automated production validation

## 🏗️ Technical Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Database      │
│   (Pages)       │◄──►│   (Functions)   │◄──►│   (D1)          │
│                 │    │                 │    │                 │
│ • Vanilla JS    │    │ • FastAPI       │    │ • SQLite        │
│ • Chart.js      │    │ • JWT Auth      │    │ • Migrations    │
│ • WebSocket     │    │ • Rate Limiting │    │ • Audit Logs    │
│ • i18n          │    │ • CORS          │    │ • Sessions      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Real-time       │    │ Async Queue     │    │ Behavioral      │
│ Updates         │    │ Processing      │    │ Detection       │
│                 │    │                 │    │                 │
│ • WebSocket     │    │ • Webhooks       │    │ • Correlation   │
│ • Broadcasting  │    │ • Retry Logic   │    │ • ECS Schema    │
│ • Live Metrics  │    │ • Multi-platform│    │ • Time Windows  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Local Development

```bash
# Clone and setup
git clone https://github.com/Garcez7R/heimdall-gatekeeper.git
cd heimdall-gatekeeper

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run development server
uvicorn backend.api.main:app --reload
```

**Access:**
- **Dashboard**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/api/system/health

### Demo Bootstrap

```bash
# Bootstrap demo data
curl http://127.0.0.1:8000/api/demo/bootstrap
```

**Demo Credentials:**
- **Admin**: `admin` / `admin123`
- **Analyst**: `analyst` / `analyst123`

### Docker Deployment

```bash
# Build and run
docker build -t heimdall-gatekeeper .
docker run -p 8000:8000 heimdall-gatekeeper
```

## ☁️ Cloudflare Production Deployment

### Prerequisites
```bash
# Install Wrangler CLI
npm install -g wrangler

# Authenticate
wrangler auth login
```

### Automated Deployment

```bash
# Run complete deployment
bash cloudflare/deploy.sh
```

### Manual Deployment

```bash
# 1. Create D1 Database
npx wrangler d1 create heimdall-db

# 2. Run Migrations
bash cloudflare/migrate-d1.sh

# 3. Deploy Functions (API)
npx wrangler deploy

# 4. Deploy Pages (Frontend)
cd frontend
npx wrangler pages deploy . --project-name=heimdall-gatekeeper-frontend
cd ..
```

### Production Testing

```bash
# Run production validation
bash cloudflare/test-production.sh
```

## 🔧 API Reference

### Authentication
```bash
# Login
POST /api/auth/login
{
  "username": "admin",
  "password": "admin123"
}

# Response
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### Webhooks (Admin Only)
```bash
# List webhooks
GET /api/webhooks

# Create webhook
POST /api/admin/webhooks
Authorization: Bearer <token>
{
  "name": "Discord Alerts",
  "url": "https://discord.com/api/webhooks/...",
  "platform": "discord",
  "severity_filter": "high",
  "active": true
}
```

### Real-time Updates
```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://your-domain.workers.dev/ws/live?token=<jwt>');

// Listen for updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'alert') {
    // Handle new alert
  }
};
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov-report=html

# Run specific test
pytest tests/test_webhooks.py::test_login_endpoint -v
```

## 📊 Monitoring & Observability

### Health Checks
- **System Health**: `/api/system/health`
- **API Status**: `/api/config`
- **Rate Limits**: Check `X-RateLimit-*` headers

### Logging
- **Structured JSON logs** in production
- **Request/Response tracking** with timing
- **Error categorization** with context

### Metrics
- **Events per minute** tracking
- **Alert volume** monitoring
- **Webhook delivery** success rates

## 🔒 Security Features

- **JWT Authentication** with configurable expiration
- **Role-based Access Control** (admin/analyst)
- **Rate Limiting** (600 req/hour default)
- **CORS Protection** with origin validation
- **Input Validation** with Pydantic schemas
- **SQL Injection Prevention** via parameterized queries
- **XSS Protection** with content sanitization

## 🌍 Internationalization

Supported languages:
- **Portuguese (BR)**: `pt-BR`
- **English**: `en`
- **Spanish**: `es`

Language switching available in dashboard preferences.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📚 Documentation

- **[API Examples](./API_EXAMPLES.md)**: Complete API usage guide
- **[Implementation Roadmap](./IMPLEMENTATION_ROADMAP.md)**: Technical evolution plan
- **[Portuguese README](./README.pt-BR.md)**: Documentação em português
- **[Spanish README](./README.es.md)**: Documentación en español

## 🏆 Why This Project Matters

Heimdall Gatekeeper demonstrates **enterprise-grade security engineering**:

| Competency | Implementation |
|---|---|
| **Detection Engineering** | YAML rules, MITRE mapping, behavioral correlation |
| **Threat Intelligence** | CVE enrichment, webhook notifications, ECS normalization |
| **Incident Response** | Alert triage, real-time updates, audit logging |
| **Infrastructure Security** | JWT auth, rate limiting, CORS, input validation |
| **Cloud Architecture** | Serverless deployment, distributed database, CDN |
| **DevSecOps** | CI/CD pipeline, automated testing, security headers |

## 📄 License

All rights reserved. Unauthorized use, modification, copying, or distribution is prohibited.

---

<p align="center">
  <strong>Built with ❤️ for SOC teams worldwide</strong><br>
  <em>Enterprise-grade security operations, simplified.</em>
</p>