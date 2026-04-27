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

## 🧪 Estratégia de Teste Real e Validação de Produção

### Visão Geral dos Testes

Esta seção detalha uma estratégia abrangente de testes para validar o Heimdall Gatekeeper em ambiente de produção, garantindo alta disponibilidade, performance e segurança.

### 1. **Testes de Funcionalidade (Unitários + Integração)**

#### Configuração do Ambiente de Teste
```bash
# Ambiente isolado com Docker
docker run -d --name heimdall-test \
  -p 8000:8000 \
  -e JWT_SECRET=test-secret-key \
  -e REDIS_HOST=redis-test \
  -v $(pwd)/tests:/app/tests \
  heimdall-gatekeeper

# Redis para testes
docker run -d --name redis-test -p 6379:6379 redis:alpine
```

#### Casos de Teste Críticos
```python
# tests/test_production_readiness.py
def test_full_security_pipeline():
    """Testa pipeline completo: ingestão → detecção → alerta → webhook"""
    # 1. Ingestão de evento
    event = create_test_event(ip="192.168.1.100", severity="high")
    response = client.post("/api/events/ingest", json=event)
    assert response.status_code == 200

    # 2. Verificação de detecção
    alerts = get_active_alerts()
    assert len(alerts) > 0
    assert alerts[0]["severity"] == "high"

    # 3. Verificação de webhook delivery
    webhook_calls = get_webhook_delivery_log()
    assert len(webhook_calls) > 0
    assert webhook_calls[0]["status"] == "delivered"

    # 4. Verificação de audit trail
    audit_events = get_audit_events(event_type="alert_generated")
    assert len(audit_events) > 0
```

### 2. **Testes de Performance e Carga**

#### Benchmarking de Ingestão
```bash
# Teste de carga com 1000 eventos/segundo
ab -n 10000 -c 100 \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -T "application/json" \
  -p test_event.json \
  http://localhost:8000/api/events/ingest

# Resultado esperado: < 500ms response time, 0% errors
```

#### Teste de Memória e CPU
```bash
# Monitoramento durante carga
docker stats heimdall-test

# Memory leak test (1 hora)
while true; do
  curl -X POST http://localhost:8000/api/events/ingest \
    -H "Content-Type: application/json" \
    -d @test_event.json
  sleep 1
done

# CPU profiling
python -m cProfile -s cumtime backend/api/main.py
```

### 3. **Testes de Segurança e Compliance**

#### Penetration Testing
```bash
# SQL Injection attempts
sqlmap -u "http://localhost:8000/api/events?filter=*" --batch

# XSS attempts
curl -X POST http://localhost:8000/api/events/ingest \
  -H "Content-Type: application/json" \
  -d '{"message": "<script>alert(1)</script>"}'

# Rate limiting test
for i in {1..700}; do
  curl http://localhost:8000/api/system/health
done
# Should return 429 after 600 requests
```

#### Compliance Validation
```python
def test_sox_compliance():
    """Valida compliance SOX/HIPAA"""
    # Test audit trail completeness
    audit_events = get_audit_trail(last_24h=True)
    required_events = ["user_login", "config_change", "data_access"]

    for event_type in required_events:
        assert event_type in [e["event_type"] for e in audit_events]

    # Test data retention
    old_audit_events = get_audit_trail(days_ago=400)
    assert len(old_audit_events) == 0  # Should be cleaned up

    # Test encryption at rest
    sensitive_data = get_encrypted_data()
    assert is_properly_encrypted(sensitive_data)
```

### 4. **Testes de Alta Disponibilidade**

#### Failover Testing
```bash
# Redis failover
docker stop redis-test
# System should continue with degraded performance
curl http://localhost:8000/api/system/health
# Should return 200 with redis_status: "degraded"

# Database failover (Cloudflare D1)
# Simulate network partition
iptables -A OUTPUT -d d1-api.cloudflare.com -j DROP
# System should queue events and retry
```

#### Chaos Engineering
```python
# tests/test_chaos.py
def test_chaos_webhook_failure():
    """Testa falha de webhooks externos"""
    # Configure webhook para URL inexistente
    configure_webhook("discord", "http://nonexistent.url")

    # Envie alerta
    create_alert(severity="critical")

    # Verifique retry logic
    delivery_attempts = get_webhook_attempts()
    assert len(delivery_attempts) >= 3  # Max retries
    assert delivery_attempts[-1]["status"] == "failed"
```

### 5. **Testes de Integração com SIEMs**

#### Splunk Integration Test
```bash
# Configurar HEC (HTTP Event Collector)
curl -X POST https://splunk-server:8088/services/collector \
  -H "Authorization: Splunk $HEC_TOKEN" \
  -d '{"event": "test_event", "source": "heimdall"}'

# Verificar no Splunk
# Search: source="heimdall" | stats count
```

#### ELK Stack Integration
```bash
# Enviar para Elasticsearch
curl -X POST "elasticsearch:9200/heimdall-events/_doc" \
  -H "Content-Type: application/json" \
  -d @test_event.json

# Verificar indexação
curl "elasticsearch:9200/_cat/indices/heimdall-*"
```

### 6. **Testes de Threat Intelligence**

#### Feed Validation
```python
def test_threat_intel_accuracy():
    """Valida precisão dos feeds de threat intel"""
    known_malicious_ip = "8.8.8.8"  # Google DNS (safe)

    # Enrich IP
    enrichment = threat_intel.enrich_ip(known_malicious_ip)

    # Should not be flagged as malicious
    assert enrichment["malicious_score"] < 50

    # Test cache
    cached = redis_cache.get_threat_intel(f"otx_ip_{known_malicious_ip}")
    assert cached is not None
```

### 7. **Testes de UI/UX**

#### E2E Testing com Playwright
```python
# tests/test_e2e.py
def test_dashboard_workflow():
    """Testa workflow completo do dashboard"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Login
        page.goto("http://localhost:8000")
        page.fill("#username", "admin")
        page.fill("#password", "admin123")
        page.click("#login-btn")

        # Verify dashboard loads
        assert page.locator(".dashboard-container").is_visible()

        # Create custom dashboard
        page.click("#create-dashboard")
        page.fill("#dashboard-name", "Test Dashboard")
        page.click("#save-dashboard")

        # Add widget
        page.click("#add-widget")
        page.select_option("#widget-type", "alert_summary")
        page.click("#add-widget-confirm")

        # Verify widget appears
        assert page.locator(".widget-alert-summary").is_visible()

        browser.close()
```

### 8. **Testes de Backup e Recovery**

#### Backup Validation
```bash
# Criar backup
sqlite3 data/heimdall.db ".backup backup.db"

# Verificar integridade
sqlite3 backup.db "PRAGMA integrity_check;"

# Testar restore
cp backup.db data/heimdall_restored.db
# Verificar se dados estão intactos
```

### 9. **Monitoramento de Testes**

#### Métricas de Teste
```python
# tests/test_monitoring.py
def test_prometheus_metrics():
    """Valida exposição de métricas Prometheus"""
    response = requests.get("http://localhost:9090/metrics")
    metrics = response.text

    # Verificar métricas críticas
    assert "heimdall_events_processed_total" in metrics
    assert "heimdall_alerts_generated_total" in metrics
    assert "heimdall_api_requests_total" in metrics

    # Verificar valores não-zero
    lines = metrics.split('\n')
    for line in lines:
        if line.startswith('heimdall_events_processed_total'):
            value = float(line.split(' ')[1])
            assert value > 0
```

### 10. **Plano de Rollback**

#### Estratégia de Rollback
```bash
# Rollback script
#!/bin/bash
echo "Iniciando rollback..."

# Parar aplicação
docker stop heimdall-prod

# Restaurar backup
cp backup_pre_deploy.db data/heimdall.db

# Reverter código
git checkout HEAD~1

# Reiniciar
docker start heimdall-prod

echo "Rollback concluído"
```

### Checklist de Produção

#### Pré-Deploy
- [ ] Todos os testes passando (pytest + coverage > 90%)
- [ ] Security scan limpo (bandit, safety)
- [ ] Performance benchmarks atingidos
- [ ] Documentação atualizada
- [ ] Backup do banco criado

#### Durante Deploy
- [ ] Blue-green deployment
- [ ] Health checks passando
- [ ] Métricas monitoradas
- [ ] Rollback plan ready

#### Pós-Deploy
- [ ] Funcionalidades críticas testadas
- [ ] Alertas de monitoramento configurados
- [ ] Equipe notificada
- [ ] Métricas baseline estabelecidas

### Métricas de Sucesso

| Métrica | Target | Critical |
|---------|--------|----------|
| Uptime | 99.9% | > 99.5% |
| Response Time (P95) | < 500ms | < 2s |
| Error Rate | < 0.1% | < 1% |
| Data Loss | 0% | < 0.01% |
| Security Incidents | 0 | < 1/month |

Esta estratégia garante que o Heimdall Gatekeeper esteja pronto para produção com alta confiança e minimizando riscos de incidentes em produção.

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