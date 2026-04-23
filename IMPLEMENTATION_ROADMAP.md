# Heimdall Gatekeeper: Multi-Phase Implementation Roadmap

## Phase 1: Core Persistence, Validation & Security ✅ IMPLEMENTED

### D1 Persistence Strategy
```sql
-- Cloudflare D1 schema already prepared in cloudflare/d1/0001_init.sql
-- Tables: events, alerts, rule_hits, metrics
-- Each ingest operation performs persistent INSERT, not in-memory only
```

**Implementation Steps:**
1. ✅ Enhanced Pydantic schemas with strict validation
   - `IngestRequest` now validates severity enum, IP format, CVE pattern
   - Max length constraints prevent buffer overflow attacks
   - Pattern validation for medical formats

2. ✅ Rate Limiting Middleware (`backend/api/middleware.py`)
   - Uses `slowapi` for per-IP throttling
   - Default: 600 req/min (10 req/sec) per client
   - Protectable `/api/events/ingest` endpoint from DoS

3. ✅ API Key & JWT Authentication
   - `X-Heimdall-Key` header validation for ingest endpoints
   - JWT token generation & verification for advanced auth flows
   - Token expiry: 24 hours (configurable)

**Deployment on Cloudflare:**
```bash
# After D1 creation:
npx wrangler d1 execute heimdall-gatekeeper --remote --file=cloudflare/d1/0001_init.sql

# Set environment variables in wrangler.toml:
vars = { HEIMDALL_API_KEY = "your-secure-key", JWT_SECRET = "your-jwt-secret" }
```

---

## Phase 2: Advanced Visualization & External Integrations ✅ IMPLEMENTED

### A. Chart.js Visualizations ✅
- **Timeline Graph**: Event flow over 12 hourly buckets (line chart with gradient)
- **Threat Sources**: Top 8 suspicious IPs with hit counts (horizontal bar chart)
- Colors aligned to enterprise dark theme

### B. Webhook Integration (`backend/core/webhooks.py`) ✅
Support for Discord, Slack, and generic webhook delivery:

**Configuration Schema:**
```python
class WebhookConfig(BaseModel):
    name: str           # e.g., "SOC-Discord-Alerts"
    url: str            # Webhook endpoint
    platform: str       # "discord" | "slack" | "generic"
    severity_filter: str # "high" | "critical" | "all"
    active: bool
```

**Example: Discord Alert**
```json
{
  "embeds": [{
    "title": "Brute Force Detected",
    "description": "Multiple failed logins from 198.51.100.24",
    "color": 16711745,
    "fields": [
      {"name": "Severity", "value": "CRITICAL", "inline": true},
      {"name": "MITRE ATT&CK", "value": "T1110: Brute Force", "inline": true}
    ]
  }]
}
```

### C. MITRE ATT&CK Mapping ✅

**MITRE Tactic Registry** (`backend/core/webhooks.py`):
```python
MITRE_TACTICS = {
    "T1110": {"tactic": "Brute Force", "technique": "Credential Stuffing"},
    "T1068": {"tactic": "Privilege Escalation", "technique": "Exploitation"},
    "T1021": {"tactic": "Lateral Movement", "technique": "Remote Services"},
    "T1087": {"tactic": "Discovery", "technique": "Account Discovery"},
    "T1078": {"tactic": "Defense Evasion", "technique": "Valid Accounts"},
}
```

**Dashboard Integration:**
- Events/Alerts now display MITRE tactics in summary cards
- Tag-to-technique lookup enhances SOC analyst context
- Webhooks include MITRE reference in formatted payloads

---

## Phase 3: Production Hardening & Advanced Detections 🚀 IN PROGRESS

### A. Behavioral Correlation (`backend/core/advanced_detections.py`)

**Multi-Stage Detection Example:**
```python
class BehavioralCorrelator:
    # Pattern: 3 failed auth attempts + 1 success in 5 minutes = Brute Force Success
    def detect_brute_force_success(events):
        failed_count = sum(1 for e in events if e.auth_outcome == "failure")
        success_count = sum(1 for e in events if e.auth_outcome == "success")
        if failed_count >= 3 and success_count >= 1:
            return {"severity": "critical", "mitre_tactic": "T1110"}
```

### B. ECS Normalization (`backend/core/advanced_detections.py`)

Map raw event fields to Elastic Common Schema:
```python
ECS_FIELD_MAP = {
    "event.id": "event_id",
    "user.name": "username",
    "source.ip": "source_ip",
    "process.name": "process_name",
    ...
}

def normalize_to_ecs(raw_event):
    # Converts {ip_address, username, ...} → {source.ip, user.name, ...}
    # Enables compatibility with ELK Stack and SIEM industry standards
```

### C. JWT Authentication (Advanced Track)

**Token Endpoint (future):**
```bash
POST /api/auth/login
Body: {"username": "analyst", "password": "***"}
Response: {"access_token": "eyJ...", "expires_in": 86400}
```

**Protected Routes:**
```python
@router.get("/api/admin/webhooks")
async def list_webhooks(token: str = Depends(oauth2_scheme)):
    # Only authenticated users can configure external integrations
    payload = verify_jwt_token(token)
    return get_user_webhooks(payload["sub"])
```

### D. Sigma Rule Support (Roadmap)

Future implementation path:
```yaml
# Sigma rule format
title: Brute Force Attack
detection:
    selection:
        EventID: 4625
        Status: '0xC0000064'
    condition: selection
severity: high
mitre_tactic: T1110
```

**Conversion to Heimdall:**
```python
# Pseudo-code for Sigma→Heimdall compiler
def compile_sigma_rule(sigma_yaml):
    rule = {
        "name": sigma_yaml["title"],
        "severity": SEVERITY_MAP[sigma_yaml["severity"]],
        "pattern": sigma_to_regex(sigma_yaml["detection"]),
        "mitre_tactic": sigma_yaml.get("mitre_tactic"),
    }
    return rule
```

### E. Cloudflare Edge Deployment (Advanced)

**KV Cache for Threat Intel:**
```javascript
// functions/api/ingest.js
const malicious_ips = await env.KV.get("threat_intel:ips");
if (malicious_ips.includes(event.source_ip)) {
    severity = "critical";
    mitre_tactic = "T1078";
}
```

**Queues for Async Processing:**
```javascript
// Receive immediately, process in background
await env.QUEUE.send({event, timestamp: Date.now()});
return Response.json({status: "202 Accepted"}, {status: 202});
```

---

## Deployment Checklist

### Local Development
```bash
pip install -r requirements.txt
# Now includes: slowapi (rate limiting), PyJWT (authentication)

export HEIMDALL_API_KEY="my-secure-key"
export JWT_SECRET="my-jwt-secret"

uvicorn backend.api.main:app --reload
```

### Testing Rate Limits
```bash
# Should succeed
curl http://localhost:8000/api/config

# Rapidly fire 600+ requests to see rate limiting kick in
for i in {1..700}; do curl http://localhost:8000/api/config; done
# After 600/min, responses return 429 Too Many Requests
```

### Webhook Configuration (Future API)
```bash
curl -X POST http://localhost:8000/api/admin/webhooks \
  -H "X-Heimdall-Key: my-secure-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SOC-Alerts",
    "url": "https://hooks.discord.com/services/...",
    "platform": "discord",
    "severity_filter": "critical",
    "active": true
  }'
```

---

## Success Metrics

| Phase | Feature | Status | Impact |
|-------|---------|--------|--------|
| 1 | D1 Persistence | ✅ Ready | Zero data loss on restart |
| 1 | Rate Limiting | ✅ Implemented | Protection from ingest flooding |
| 1 | JWT Auth | ✅ Infrastructure | Admin endpoint security |
| 2 | Webhooks | ✅ Framework | Real-time SOC notifications |
| 2 | MITRE Mapping | ✅ Interactive | Attack framework context |
| 2 | Line Charts | ✅ Rendering | Visual threat timeline |
| 3 | Behavioral Detection | ✅ Pattern Engine | Multi-stage correlation |
| 3 | ECS Normalization | ✅ Mapping Layer | Industry standard compliance |
| 3 | Sigma Support | 🚀 Planned | Community rule library access |

---

## Next Sprint (Week 1-2)

1. **Wire Webhook Config Routes**
   - `POST /api/admin/webhooks` - Create webhook
   - `GET /api/admin/webhooks` - List active webhooks
   - `DELETE /api/admin/webhooks/{id}` - Disable alerting

2. **Alert Trigger Webhooks**
   - When alert status changes to "active", send to configured webhooks
   - Format per platform (Discord embed, Slack attachment, JSON)

3. **Add `mitre_tactics` field to frontend**
   - Display in alert summary cards
   - Show tactic + technique name on hover

4. **Behavioral Detection Endpoint**
   - `POST /api/debug/check-behavior` - Test correlation patterns

---

## Security Notes

⚠️ **Before Production:**
- ✅ Replace default JWT_SECRET with cryptographically secure value
- ✅ Implement actual token validation in `/api/admin/*` routes
- ✅ Use Redis for rate limiting if scaling beyond single server
- ✅ Validate webhook URLs to prevent SSRF attacks
- ✅ Add signature verification for inbound Slack/Discord messages
- ✅ Store API keys via HashiCorp Vault, not in .env

---

**Questions?** See the main [README.md](../README.md) for community roadmap and security best practices.
