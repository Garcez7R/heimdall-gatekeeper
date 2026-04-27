# Heimdall Gatekeeper API Examples

## Table of Contents
- [Phase 1: Authentication & Rate Limiting](#phase-1-authentication--rate-limiting)
- [Phase 2: Webhooks & MITRE Mapping](#phase-2-webhooks--mitre-mapping)
- [Phase 3: Advanced Detections](#phase-3-advanced-detections)

---

## Phase 1: Authentication & Rate Limiting

### API Key Authentication

All ingest endpoints require the `X-Heimdall-Key` header:

```bash
curl -X POST http://localhost:8000/api/events/ingest \
  -H "X-Heimdall-Key: my-secure-key" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "auth-gateway",
    "event_type": "failed_login",
    "title": "Failed Login Attempt",
    "message": "User admin failed to authenticate from 198.51.100.24",
    "severity": "high",
    "ip_address": "198.51.100.24",
    "mitre_tactics": ["T1110"]
  }'
```

**Response:**
```json
{
  "event_id": "evt_abc123",
  "alert_ids": ["alr_xyz789"],
  "severity": "high",
  "rule_matched": "Brute Force Attempt"
}
```

### JWT Token Exchange (Advanced)

Generate a JWT token for programmatic access:

```python
from backend.api.middleware import create_jwt_token, verify_jwt_token

# Create token valid for 24 hours
token = create_jwt_token({"sub": "analyst@company.com", "role": "admin"})
# Returns: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Verify token
payload = verify_jwt_token(token)
# Returns: {"sub": "analyst@company.com", "role": "admin", "exp": ...}
```

### Rate Limiting

- **Limit**: 600 requests per minute per IP (10 req/sec)
- **Response** when exceeded: `429 Too Many Requests`

```bash
# Exceed rate limit
for i in {1..700}; do curl http://localhost:8000/api/config; done

# Response on 601st request:
# HTTP/1.1 429 Too Many Requests
# {"detail": "429: Too Many Requests"}
```

---

## Phase 2: Webhooks & MITRE Mapping

### MITRE ATT&CK Tactic Reference

Events can now include MITRE ATT&CK tactics for threat intelligence context:

| Tactic ID | Tactic Name | Technique |
|-----------|-------------|-----------|
| T1110 | Brute Force | Credential Stuffing |
| T1068 | Privilege Escalation | Exploitation for Privilege Escalation |
| T1021 | Lateral Movement | Remote Services |
| T1087 | Discovery | Account Discovery |
| T1078 | Defense Evasion | Valid Accounts |

### Ingest Event with MITRE Context

```bash
curl -X POST http://localhost:8000/api/events/ingest \
  -H "X-Heimdall-Key: my-secure-key" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "endpoint-detection",
    "event_type": "privilege_escalation",
    "title": "Privilege Escalation Detected",
    "message": "Process explorer.exe executed with SYSTEM privileges from user context",
    "severity": "critical",
    "mitre_tactics": ["T1068", "T1078"]
  }'
```

### Configure Webhook (Future Endpoint)

```bash
curl -X POST http://localhost:8000/api/admin/webhooks \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SOC-Discord-Bridge",
    "url": "https://discordapp.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN",
    "platform": "discord",
    "severity_filter": "critical",
    "active": true
  }'
```

### Webhook Alert Format (Discord)

When a critical alert fires, Heimdall sends:

```json
{
  "embeds": [{
    "title": "Privilege Escalation Detected",
    "description": "Process explorer.exe executed with SYSTEM privileges from user context",
    "color": 16711745,
    "fields": [
      {
        "name": "Severity",
        "value": "CRITICAL",
        "inline": true
      },
      {
        "name": "Rule",
        "value": "Privilege Escalation Attempt",
        "inline": true
      },
      {
        "name": "MITRE ATT&CK",
        "value": "T1068: Exploitation for Privilege Escalation",
        "inline": false
      },
      {
        "name": "Source",
        "value": "endpoint-detection",
        "inline": true
      }
    ]
  }]
}
```

### Webhook Alert Format (Slack)

```json
{
  "attachments": [{
    "color": "#FF5555",
    "title": "Privilege Escalation Detected",
    "text": "Process explorer.exe executed with SYSTEM privileges from user context",
    "fields": [
      {
        "title": "Severity",
        "value": "CRITICAL",
        "short": true
      },
      {
        "title": "MITRE ATT&CK",
        "value": "T1068: Exploitation for Privilege Escalation",
        "short": false
      }
    ],
    "footer": "Heimdall Gatekeeper"
  }]
}
```

---

## Phase 3: Advanced Detections

### Behavioral Correlation Pattern

Detect a brute force attack followed by successful authentication:

```python
from backend.core.advanced_detections import BehavioralCorrelator

correlator = BehavioralCorrelator(window_minutes=5, group_by="user_name")

# Feed failed authentication events
for attempt in [1, 2, 3]:  # 3 failed attempts
    event = {
        "user_name": "admin",
        "event_type": "authentication",
        "auth_outcome": "failure"
    }
    correlator.add_event(event)

# Feed successful authentication
success_event = {
    "user_name": "admin",
    "event_type": "authentication",
    "auth_outcome": "success"
}
detection = correlator.add_event(success_event)

# Returns:
# {
#   "detection": "Brute Force with Success",
#   "severity": "critical",
#   "group_key": "admin",
#   "failed_attempts": 3,
#   "successes": 1,
#   "mitre_tactic": "T1110"
# }
```

### ECS Field Normalization

Map raw events to Elastic Common Schema:

```python
from backend.core.advanced_detections import normalize_to_ecs

raw_event = {
    "id": "evt_123",
    "username": "john.doe",
    "source_ip": "192.168.1.100",
    "event_type": "login",
    "severity": "medium",
    "message": "User successfully authenticated"
}

ecs_event = normalize_to_ecs(raw_event)

# Returns:
# {
#   "event.id": "evt_123",
#   "event.category": "process",
#   "event.action": "login",
#   "event.severity": 5,
#   "user.name": "john.doe",
#   "source.ip": "192.168.1.100",
#   "message": "User successfully authenticated"
# }
```

### Sigma Rule Parsing (Roadmap)

Example of converting industry-standard Sigma rules:

```yaml
title: Brute Force Attack
detection:
  selection:
    EventID: 4625
    Status: '0xC0000064'
  timeframe: 5m
  condition: selection | count > 3
severity: high
mitre_tactic: T1110
```

**Converted to Heimdall format:**
```yaml
name: "Brute Force Attack"
detection:
  - field: "event_type"
    pattern: "^authentication_failure$"
  - field: "source"
    pattern: ".*"
timeframe_minutes: 5
alert_count_threshold: 3
severity: "high"
mitre_tactic: "T1110"
```

---

## Testing & Validation

### Validate Payload Strictness

```bash
# Missing required field - should fail
curl -X POST http://localhost:8000/api/events/ingest \
  -H "X-Heimdall-Key: my-secure-key" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "test",
    "event_type": "test"
    # Missing: title, message, severity
  }'

# Response:
# HTTP/1.1 422 Unprocessable Entity
# {
#   "detail": [
#     {
#       "loc": ["body", "title"],
#       "msg": "Field required",
#       "type": "missing"
#     }
#   ]
# }
```

### CVE Pattern Validation

```bash
# Valid CVE format
curl -X POST http://localhost:8000/api/events/ingest \
  -H "X-Heimdall-Key: my-secure-key" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "scanner",
    "event_type": "vuln_found",
    "title": "CVE Detected",
    "message": "System vulnerable to known exploit",
    "severity": "critical",
    "cve_id": "CVE-2024-3094"
  }'

# Invalid CVE format - should fail
curl -X POST http://localhost:8000/api/events/ingest \
  -H "X-Heimdall-Key: my-secure-key" \
  -H "Content-Type: application/json" \
  -d '{
    "cve_id": "INVALID-CVE"
  }'
# Response: HTTP/1.1 422 - Pattern validation failed
```

---

## Environment Setup

### Local Development

```bash
export HEIMDALL_API_KEY="your-production-key-here"
export JWT_SECRET="your-jwt-secret-here"
uvicorn backend.api.main:app --reload
```

### Docker & Cloudflare

See [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md) for full deployment setup.
