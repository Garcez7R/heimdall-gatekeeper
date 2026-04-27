CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  event_type TEXT NOT NULL,
  severity TEXT NOT NULL DEFAULT 'low',
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  raw_payload TEXT,
  ip_address TEXT,
  cve_id TEXT,
  cve_score REAL,
  status TEXT NOT NULL DEFAULT 'new',
  tags TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rule_name TEXT NOT NULL,
  severity TEXT NOT NULL,
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  source TEXT NOT NULL,
  event_id INTEGER,
  ip_address TEXT,
  cve_id TEXT,
  cve_score REAL,
  mitre_tag TEXT,
  status TEXT NOT NULL DEFAULT 'active',
  acknowledged_by TEXT,
  resolved_by TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rule_hits (
  rule_name TEXT PRIMARY KEY,
  total_hits INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cve_cache (
  cve_id TEXT PRIMARY KEY,
  score REAL,
  severity TEXT,
  summary TEXT,
  payload TEXT,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_metrics (
  metric_key TEXT PRIMARY KEY,
  metric_value TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Webhooks table for persistent webhook configuration
CREATE TABLE IF NOT EXISTS webhooks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  webhook_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  platform TEXT NOT NULL DEFAULT 'generic',
  severity_filter TEXT,
  active INTEGER NOT NULL DEFAULT 1,
  headers TEXT,  -- JSON string of custom headers
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Audit trail for compliance (SOX/HIPAA)
CREATE TABLE IF NOT EXISTS audit_trail (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_type TEXT NOT NULL,
  user_id TEXT NOT NULL,
  severity TEXT NOT NULL,
  resource_type TEXT NOT NULL,
  resource_id TEXT NOT NULL,
  action TEXT NOT NULL,
  details TEXT,  -- JSON string
  ip_address TEXT,
  user_agent TEXT,
  session_id TEXT,
  timestamp TEXT NOT NULL
);

-- Custom dashboards for users
CREATE TABLE IF NOT EXISTS user_dashboards (
  dashboard_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  dashboard_name TEXT NOT NULL,
  is_default INTEGER NOT NULL DEFAULT 0,
  widgets TEXT NOT NULL,  -- JSON string of widgets array
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- User sessions for JWT management
CREATE TABLE IF NOT EXISTS user_sessions (
  session_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  ip_address TEXT,
  user_agent TEXT,
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  last_activity TEXT NOT NULL
);

-- Data retention policies
CREATE TABLE IF NOT EXISTS data_retention_policies (
  policy_id TEXT PRIMARY KEY,
  table_name TEXT NOT NULL,
  retention_days INTEGER NOT NULL,
  enabled INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

-- Threat intelligence cache
CREATE TABLE IF NOT EXISTS threat_intel_cache (
  cache_key TEXT PRIMARY KEY,
  intel_type TEXT NOT NULL,
  data TEXT NOT NULL,  -- JSON string
  source TEXT NOT NULL,
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_created_at ON events (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_severity ON events (severity);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts (status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts (severity, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_trail_timestamp ON audit_trail (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_trail_user ON audit_trail (user_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_trail_event ON audit_trail (event_type, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_webhooks_active ON webhooks (active, platform);
CREATE INDEX IF NOT EXISTS idx_user_dashboards_user ON user_dashboards (user_id, is_default DESC);
CREATE INDEX IF NOT EXISTS idx_threat_intel_expires ON threat_intel_cache (expires_at);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires ON user_sessions (expires_at);
