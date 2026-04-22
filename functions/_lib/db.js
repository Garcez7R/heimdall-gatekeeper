import { demoEvents } from "./demo.js";

const ruleDefinitions = [
  {
    name: "Brute Force Detection",
    pattern: /(failed login|invalid password|authentication failure)/i,
    severity: "high",
    title: "Brute force suspected",
    description: "Multiple authentication failures detected in the same signal path.",
    mitre_tag: "T1110",
    source_contains: "auth",
  },
  {
    name: "Suspicious Privilege Escalation",
    pattern: /(sudo|privilege escalation|admin role granted|administrative privileges)/i,
    severity: "critical",
    title: "Privilege escalation signal",
    description: "Sensitive role escalation or administrative elevation was detected.",
    mitre_tag: "T1068",
  },
  {
    name: "Known Vulnerability Reference",
    pattern: /CVE-\d{4}-\d{4,7}/i,
    severity: "medium",
    title: "CVE reference observed",
    description: "An event carries a vulnerability identifier and should be enriched with threat intelligence.",
    mitre_tag: "T1595",
  },
];

function nowIso() {
  return new Date().toISOString();
}

function normalizeSeverity(value) {
  const severity = String(value || "low").toLowerCase();
  return ["low", "medium", "high", "critical"].includes(severity) ? severity : "low";
}

function sanitizePayload(payload) {
  const cleaned = {
    source: String(payload.source || "unknown").trim().slice(0, 120),
    event_type: String(payload.event_type || payload.type || "generic").trim().slice(0, 120),
    title: String(payload.title || "Generic event").trim().slice(0, 180),
    message: String(payload.message || payload.description || "No message provided").trim().slice(0, 2000),
    severity: normalizeSeverity(payload.severity),
    ip_address: payload.ip_address ? String(payload.ip_address).trim().slice(0, 64) : null,
    cve_id: payload.cve_id ? String(payload.cve_id).trim().toUpperCase() : null,
    tags: Array.isArray(payload.tags) ? payload.tags.map((item) => String(item).trim().slice(0, 40)) : String(payload.tags || "").split(",").filter(Boolean),
  };

  if (cleaned.cve_id && !/^CVE-\d{4}-\d{4,7}$/i.test(cleaned.cve_id)) {
    cleaned.cve_id = null;
  }

  return cleaned;
}

export async function ensureSeed(env) {
  const row = await env.DB.prepare("SELECT COUNT(*) AS total FROM events").first();
  if (Number(row?.total || 0) > 0) return;
  for (const event of demoEvents) {
    await ingestEvent(env, event);
  }
}

export async function ingestEvent(env, payload) {
  const event = sanitizePayload(payload);
  const createdAt = nowIso();
  const inserted = await env.DB.prepare(
    `INSERT INTO events
      (source, event_type, severity, title, message, raw_payload, ip_address, cve_id, cve_score, status, tags, created_at, updated_at)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  )
    .bind(
      event.source,
      event.event_type,
      event.severity,
      event.title,
      event.message,
      JSON.stringify(payload),
      event.ip_address,
      event.cve_id,
      null,
      "new",
      event.tags.join(","),
      createdAt,
      createdAt,
    )
    .run();

  const eventId = Number(inserted.meta.last_row_id);
  const alertIds = [];

  for (const rule of ruleDefinitions) {
    const haystack = [event.source, event.event_type, event.title, event.message, event.tags.join(",")].join(" ");
    if (rule.source_contains && !event.source.toLowerCase().includes(rule.source_contains)) continue;
    if (!rule.pattern.test(haystack)) continue;

    const alertInsert = await env.DB.prepare(
      `INSERT INTO alerts
        (rule_name, severity, title, message, source, event_id, ip_address, cve_id, cve_score, mitre_tag, status, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
      .bind(
        rule.name,
        rule.severity,
        rule.title,
        `${rule.description} | ${event.message}`,
        event.source,
        eventId,
        event.ip_address,
        event.cve_id,
        null,
        rule.mitre_tag,
        "active",
        createdAt,
        createdAt,
      )
      .run();

    alertIds.push(Number(alertInsert.meta.last_row_id));

    await env.DB.prepare(
      `INSERT INTO rule_hits (rule_name, total_hits, updated_at)
       VALUES (?, 1, ?)
       ON CONFLICT(rule_name) DO UPDATE SET
         total_hits = total_hits + 1,
         updated_at = excluded.updated_at`
    )
      .bind(rule.name, createdAt)
      .run();
  }

  await env.DB.prepare(
    `INSERT INTO system_metrics (metric_key, metric_value, updated_at)
     VALUES (?, ?, ?)
     ON CONFLICT(metric_key) DO UPDATE SET metric_value = excluded.metric_value, updated_at = excluded.updated_at`
  )
    .bind("last_ingest_at", createdAt, createdAt)
    .run();

  const eventsPerMinute = await env.DB.prepare(
    `SELECT COUNT(*) AS total FROM events WHERE created_at >= datetime('now', '-1 minute')`
  ).first();

  await env.DB.prepare(
    `INSERT INTO system_metrics (metric_key, metric_value, updated_at)
     VALUES (?, ?, ?)
     ON CONFLICT(metric_key) DO UPDATE SET metric_value = excluded.metric_value, updated_at = excluded.updated_at`
  )
    .bind("events_per_minute", String(eventsPerMinute?.total || 0), createdAt)
    .run();

  return { event_id: eventId, alert_ids: alertIds };
}

export async function overviewSnapshot(env) {
  const [eventsTotal, activeAlerts, criticalAlerts, latestAlerts, latestEvents, topSources, topCves, topIps, ruleHits, uptime, eventsPerMinute] = await Promise.all([
    env.DB.prepare("SELECT COUNT(*) AS total FROM events").first(),
    env.DB.prepare("SELECT COUNT(*) AS total FROM alerts WHERE status != 'resolved'").first(),
    env.DB.prepare("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'critical' AND status != 'resolved'").first(),
    env.DB.prepare("SELECT * FROM alerts ORDER BY created_at DESC LIMIT 8").all(),
    env.DB.prepare("SELECT * FROM events ORDER BY created_at DESC LIMIT 8").all(),
    env.DB.prepare("SELECT source, COUNT(*) AS total FROM events GROUP BY source ORDER BY total DESC, source ASC LIMIT 6").all(),
    env.DB.prepare("SELECT cve_id, COUNT(*) AS total, MAX(cve_score) AS score FROM alerts WHERE cve_id IS NOT NULL AND cve_id != '' GROUP BY cve_id ORDER BY total DESC LIMIT 6").all(),
    env.DB.prepare("SELECT ip_address, COUNT(*) AS total FROM events WHERE ip_address IS NOT NULL AND ip_address != '' GROUP BY ip_address ORDER BY total DESC LIMIT 6").all(),
    env.DB.prepare("SELECT rule_name, total_hits FROM rule_hits ORDER BY total_hits DESC LIMIT 5").all(),
    env.DB.prepare("SELECT metric_value FROM system_metrics WHERE metric_key = 'uptime_seconds'").first(),
    env.DB.prepare("SELECT metric_value FROM system_metrics WHERE metric_key = 'events_per_minute'").first(),
  ]);

  const timeline = await env.DB.prepare(
    `SELECT substr(created_at, 1, 13) || ':00' AS bucket, COUNT(*) AS total
     FROM events
     GROUP BY bucket
     ORDER BY bucket DESC
     LIMIT 12`
  ).all();

  return {
    status: {
      system: "healthy",
      uptime_seconds: Number(uptime?.metric_value || 0),
      events_total: Number(eventsTotal?.total || 0),
      active_alerts: Number(activeAlerts?.total || 0),
      critical_alerts: Number(criticalAlerts?.total || 0),
      rule_hits: ruleHits.results || [],
      metrics: [
        { metric_key: "events_per_minute", metric_value: String(eventsPerMinute?.metric_value || 0), updated_at: nowIso() },
      ],
    },
    severity_breakdown: {
      critical: Number(criticalAlerts?.total || 0),
      high: Number((await env.DB.prepare("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'high' AND status != 'resolved'").first())?.total || 0),
      medium: Number((await env.DB.prepare("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'medium' AND status != 'resolved'").first())?.total || 0),
      low: Number((await env.DB.prepare("SELECT COUNT(*) AS total FROM alerts WHERE severity = 'low' AND status != 'resolved'").first())?.total || 0),
    },
    timeline: (timeline.results || []).reverse(),
    top_sources: topSources.results || [],
    top_cves: topCves.results || [],
    events_per_minute: String(eventsPerMinute?.metric_value || 0),
    last_ingest_at: null,
    latest_alerts: latestAlerts.results || [],
    latest_events: latestEvents.results || [],
    top_ips: topIps.results || [],
  };
}

export async function listEvents(env, { search = "", severity = "", limit = 100 } = {}) {
  let sql = "SELECT * FROM events WHERE 1=1";
  const bindings = [];
  if (search) {
    sql += " AND (title LIKE ? OR message LIKE ? OR source LIKE ?)";
    const like = `%${search}%`;
    bindings.push(like, like, like);
  }
  if (severity) {
    sql += " AND severity = ?";
    bindings.push(severity);
  }
  sql += " ORDER BY created_at DESC LIMIT ?";
  bindings.push(limit);
  return env.DB.prepare(sql).bind(...bindings).all();
}

export async function listAlerts(env, { status = "", limit = 100 } = {}) {
  let sql = "SELECT * FROM alerts WHERE 1=1";
  const bindings = [];
  if (status) {
    sql += " AND status = ?";
    bindings.push(status);
  }
  sql += " ORDER BY created_at DESC LIMIT ?";
  bindings.push(limit);
  return env.DB.prepare(sql).bind(...bindings).all();
}

export async function updateAlertStatus(env, alertId, status, actor) {
  const field = status === "acknowledged" ? "acknowledged_by" : "resolved_by";
  return env.DB.prepare(
    `UPDATE alerts SET status = ?, ${field} = ?, updated_at = ? WHERE id = ?`
  )
    .bind(status, actor, nowIso(), alertId)
    .run();
}
