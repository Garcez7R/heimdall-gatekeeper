const STORAGE_KEY = "heimdall-console-preferences";
const REFRESH_INTERVAL_MS = 15000;

const state = {
  view: "overview",
  language: "pt-BR",
  theme: "dark",
  density: "comfortable",
  highContrast: false,
  reduceMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  dictionary: {},
  autoRefreshHandle: null,
  lastOverview: null,
};

let appRevealed = false;

const charts = {
  timeline: null,
  topIps: null,
};

const ingestPresets = [
  {
    source: "auth-gateway",
    event_type: "failed_login",
    title: "Repeated login failure",
    message: "Multiple failed login attempts for admin user from external IP.",
    ip_address: "198.51.100.24",
    severity: "medium",
    cve_id: "",
  },
  {
    source: "identity-core",
    event_type: "privilege_escalation",
    title: "Unexpected admin elevation",
    message: "A standard operator account received administrative privileges unexpectedly.",
    ip_address: "203.0.113.18",
    severity: "critical",
    cve_id: "",
  },
  {
    source: "vuln-scanner",
    event_type: "vulnerability_reference",
    title: "Critical edge package exposure",
    message: "Observed vulnerable package reference CVE-2024-3094 during inventory correlation.",
    ip_address: "10.10.0.17",
    severity: "high",
    cve_id: "CVE-2024-3094",
  },
];

function readStoredPreferences() {
  try {
    const payload = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    state.language = payload.language || state.language;
    state.theme = payload.theme || state.theme;
    state.density = payload.density || state.density;
    state.highContrast = Boolean(payload.highContrast);
    state.reduceMotion = payload.reduceMotion ?? state.reduceMotion;
  } catch (_error) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function persistPreferences() {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      language: state.language,
      theme: state.theme,
      density: state.density,
      highContrast: state.highContrast,
      reduceMotion: state.reduceMotion,
    })
  );
}

async function request(path, options = {}) {
  const response = await fetch(path, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.detail || body.error || `Request failed: ${response.status}`);
  }
  return body;
}

function text(key, fallback) {
  return state.dictionary[key] || fallback;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function severityBadge(severity) {
  return `<span class="badge ${severity}">${String(severity || "low").toUpperCase()}</span>`;
}

function formatDateTime(value) {
  if (!value) return "n/a";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return new Intl.DateTimeFormat(state.language, {
    dateStyle: "short",
    timeStyle: "medium",
  }).format(date);
}

function formatRelativeTime(value) {
  if (!value) return text("notAvailable", "n/a");
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  const diffSeconds = Math.round((date.getTime() - Date.now()) / 1000);
  const formatter = new Intl.RelativeTimeFormat(state.language, { numeric: "auto" });
  const abs = Math.abs(diffSeconds);
  if (abs < 60) return formatter.format(diffSeconds, "second");
  if (abs < 3600) return formatter.format(Math.round(diffSeconds / 60), "minute");
  return formatter.format(Math.round(diffSeconds / 3600), "hour");
}

function pushToast(message, tone = "error") {
  const stack = document.getElementById("toast-stack");
  const toast = document.createElement("div");
  toast.className = `toast ${tone}`;
  toast.textContent = message;
  stack.appendChild(toast);
  window.setTimeout(() => {
    toast.remove();
  }, 4200);
}

function revealApp() {
  if (appRevealed) return;
  appRevealed = true;
  const splash = document.getElementById("splash");
  if (splash) splash.hidden = true;
  const app = document.getElementById("app");
  if (app) app.hidden = false;
}

function setView(view) {
  state.view = view;
  document.querySelectorAll(".view").forEach((el) => el.classList.remove("active"));
  document.querySelectorAll(".nav-item").forEach((el) => el.classList.remove("active"));
  document.getElementById(`view-${view}`)?.classList.add("active");
  document.querySelector(`.nav-item[data-view="${view}"]`)?.classList.add("active");
  document.getElementById("view-title").textContent = text(view, view);
  document.getElementById("view-description").textContent = getViewDescription(view);
}

function getViewDescription(view) {
  const descriptions = {
    overview: text("overviewDescription", "Operational visibility for alert queue, event flow and detection coverage."),
    alerts: text("alertsDescription", "Triage, acknowledge and resolve detections with analyst-friendly context."),
    events: text("eventsDescription", "Search normalized events and inspect recent signals across monitored sources."),
    status: text("statusDescription", "Inspect engine state and inject controlled sample signals into the pipeline."),
  };
  return descriptions[view] || descriptions.overview;
}

function applyUiPreferences() {
  document.documentElement.lang = state.language;
  document.body.dataset.theme = state.theme;
  document.body.classList.toggle("compact", state.density === "compact");
  document.body.classList.toggle("high-contrast", state.highContrast);
  document.body.classList.toggle("reduce-motion", state.reduceMotion);
  document.getElementById("theme-switcher").value = state.theme;
  document.getElementById("density-switcher").value = state.density;
  document.getElementById("language-switcher").value = state.language;
  persistPreferences();
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const key = node.dataset.i18n;
    node.textContent = text(key, node.textContent);
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    const key = node.dataset.i18nPlaceholder;
    node.placeholder = text(key, node.placeholder);
  });

  document.querySelectorAll("#alert-status-filter option").forEach((option) => {
    if (option.dataset.i18n) option.textContent = text(option.dataset.i18n, option.textContent);
  });
  document.querySelectorAll("#event-severity-filter option").forEach((option) => {
    if (option.dataset.i18n) option.textContent = text(option.dataset.i18n, option.textContent);
  });

  setView(state.view);
}

function updateClock() {
  document.getElementById("live-clock").textContent = new Intl.DateTimeFormat(state.language, {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(new Date());
}

function updateConsoleHeader(overview) {
  const healthy = String(overview.status.system || "").toLowerCase() === "healthy";
  const healthLabel = healthy ? text("healthy", "Healthy") : text("degraded", "Degraded");
  document.getElementById("console-health-label").textContent = healthLabel;
  document.getElementById("console-last-sync").textContent = `${text("lastSync", "Last sync")} ${new Intl.DateTimeFormat(state.language, {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(new Date())}`;
  document.getElementById("console-note").textContent =
    overview.status.active_alerts > 0
      ? text("consoleNoteAlerting", "Alert queue is active. Review priority items and confirm triage coverage.")
      : text("consoleNoteStable", "Signal flow stable. Monitoring live ingestion, alert queue and detection pressure.");
}

function renderMetrics(overview) {
  const metrics = [
    [text("events", "Events"), overview.status.events_total, text("eventsHint", "Normalized events stored in the pipeline.")],
    [text("activeAlerts", "Active Alerts"), overview.status.active_alerts, text("activeAlertsHint", "Alerts still requiring analyst action.")],
    [text("criticalAlerts", "Critical Alerts"), overview.status.critical_alerts, text("criticalAlertsHint", "Highest urgency security detections.")],
    [text("eventsPerMinute", "Events/min"), overview.events_per_minute || "0", text("eventsPerMinuteHint", "Recent operational ingestion cadence.")],
  ];

  document.getElementById("metric-grid").innerHTML = metrics
    .map(
      ([label, value, hint]) => `
        <article class="metric">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(value)}</strong>
          <small>${escapeHtml(hint)}</small>
        </article>
      `
    )
    .join("");

  const systemHealth = document.getElementById("system-health");
  const healthLabel = overview.status.system === "healthy"
    ? text("healthy", "Healthy")
    : text("degraded", "Degraded");
  systemHealth.textContent = escapeHtml(healthLabel);
  systemHealth.className = `status-pill ${overview.status.system === "healthy" ? "healthy" : "degraded"}`;
  document.getElementById("uptime-pill").textContent = `${text("uptime", "Uptime")} ${overview.status.uptime_seconds}s`;
  document.getElementById("last-ingest-pill").textContent = `${text("lastIngest", "Last ingest")} ${formatRelativeTime(overview.last_ingest_at)}`;

  document.getElementById("ops-active-alerts").textContent = overview.status.active_alerts ?? 0;
  document.getElementById("ops-critical-alerts").textContent = overview.status.critical_alerts ?? 0;
  document.getElementById("ops-events-per-minute").textContent = overview.events_per_minute || "0";
  document.getElementById("ops-source-count").textContent = (overview.top_sources || []).length;
}

function renderRuleHits(rows) {
  const sidebar = document.getElementById("rule-hits-sidebar");
  const main = document.getElementById("rule-hits-main");
  if (!rows?.length) {
    const empty = `<div class="mini-stack-item"><strong>${escapeHtml(text("noRuleHits", "No rule activity yet"))}</strong><span>${escapeHtml(text("noRuleHitsHint", "Rules will appear here as detections trigger."))}</span></div>`;
    sidebar.innerHTML = empty;
    main.innerHTML = `<div class="stack-item">${escapeHtml(text("noRuleHitsHint", "Rules will appear here as detections trigger."))}</div>`;
    return;
  }

  sidebar.innerHTML = rows
    .slice(0, 4)
    .map(
      (row) => `
        <div class="mini-stack-item">
          <strong>${escapeHtml(row.total_hits)}</strong>
          <span>${escapeHtml(row.rule_name)}</span>
        </div>
      `
    )
    .join("");

  main.innerHTML = rows
    .map(
      (row) => `
        <article class="stack-item">
          <div class="row">
            <strong>${escapeHtml(row.rule_name)}</strong>
            <span class="meta-chip">${escapeHtml(text("hits", "Hits"))}: ${escapeHtml(row.total_hits)}</span>
          </div>
          <small>${escapeHtml(text("rulePressureHint", "Detection volume for this rule in the current dataset."))}</small>
        </article>
      `
    )
    .join("");
}

function renderLatestAlerts(rows) {
  const container = document.getElementById("latest-alerts");
  if (!rows?.length) {
    container.innerHTML = `<div class="stack-item">${escapeHtml(text("noAlerts", "No active alerts yet."))}</div>`;
    return;
  }
  container.innerHTML = rows
    .map(
      (row) => `
        <article class="stack-item">
          <div class="row">
            <strong>${escapeHtml(row.title)}</strong>
            ${severityBadge(row.severity)}
          </div>
          <span>${escapeHtml(row.message)}</span>
          <div class="event-meta">
            <span class="meta-chip">${escapeHtml(row.source || "unknown")}</span>
            <span class="meta-chip">${escapeHtml(formatRelativeTime(row.created_at))}</span>
            ${row.mitre_tag ? `<span class="meta-chip">${escapeHtml(row.mitre_tag)}</span>` : ""}
          </div>
        </article>
      `
    )
    .join("");
}

function renderLatestEvents(rows) {
  const container = document.getElementById("latest-events");
  if (!rows?.length) {
    container.innerHTML = `<div class="stack-item">${escapeHtml(text("noEvents", "No recent events yet."))}</div>`;
    return;
  }
  container.innerHTML = rows
    .map(
      (row) => `
        <article class="stack-item">
          <div class="row">
            <strong>${escapeHtml(row.title)}</strong>
            ${severityBadge(row.severity)}
          </div>
          <small>${escapeHtml(row.message)}</small>
          <div class="event-meta">
            <span class="meta-chip">${escapeHtml(row.event_type)}</span>
            <span class="meta-chip">${escapeHtml(row.source)}</span>
            <span class="meta-chip">${escapeHtml(formatRelativeTime(row.created_at))}</span>
          </div>
        </article>
      `
    )
    .join("");
}

function renderAlertsSummary(rows) {
  const total = rows.length;
  const active = rows.filter((row) => String(row.status).toLowerCase() === "active").length;
  const highSeverity = rows.filter((row) => ["high", "critical"].includes(String(row.severity).toLowerCase())).length;
  document.getElementById("alerts-summary-total").textContent = total;
  document.getElementById("alerts-summary-active").textContent = active;
  document.getElementById("alerts-summary-high").textContent = highSeverity;
}

function renderEventSourceOptions(rows) {
  const sourceSelect = document.getElementById("event-source-filter");
  const current = sourceSelect.value;
  const sources = [...new Set(rows.map((row) => row.source).filter(Boolean))].sort();
  sourceSelect.innerHTML = `<option value="">All sources</option>` +
    sources.map((source) => `<option value="${escapeHtml(source)}">${escapeHtml(source)}</option>`).join("");
  sourceSelect.value = current;
}

function renderEventsSummary(rows) {
  const total = rows.length;
  const sources = new Set(rows.map((row) => row.source).filter(Boolean)).size;
  const highSeverity = rows.filter((row) => ["high", "critical"].includes(String(row.severity).toLowerCase())).length;
  document.getElementById("events-summary-total").textContent = total;
  document.getElementById("events-summary-sources").textContent = sources;
  document.getElementById("events-summary-severity").textContent = highSeverity;
}

function renderTopIps(rows) {
  const entries = (rows || []).slice(0, 8);
  const canvasEl = document.getElementById("chart-top-ips");
  if (!canvasEl) return;

  if (!entries.length) {
    if (charts.topIps) {
      charts.topIps.destroy();
      charts.topIps = null;
    }
    canvasEl.style.display = "none";
    return;
  }

  canvasEl.style.display = "block";
  const labels = entries.map((row) => (row.ip_address || "unknown").substring(0, 15));
  const data = entries.map((row) => Number(row.total || 0));
  const ctx = canvasEl.getContext("2d");

  if (charts.topIps) charts.topIps.destroy();

  charts.topIps = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: text("hits", "Hits"),
          data,
          backgroundColor: "rgba(125, 211, 246, 0.32)",
          borderColor: "rgba(125, 211, 246, 0.72)",
          borderWidth: 1,
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      indexAxis: "y",
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: {
          ticks: { color: "rgba(255, 255, 255, 0.6)" },
          grid: { color: "rgba(255, 255, 255, 0.1)" },
        },
        y: {
          ticks: { color: "rgba(255, 255, 255, 0.6)" },
          grid: { display: false },
        },
      },
    },
  });
}

function renderTimeline(points) {
  const canvasEl = document.getElementById("chart-timeline");
  if (!canvasEl) return;

  if (!points?.length) {
    if (charts.timeline) {
      charts.timeline.destroy();
      charts.timeline = null;
    }
    canvasEl.style.display = "none";
    return;
  }

  canvasEl.style.display = "block";
  const labels = points.map((item) => String(item.bucket).slice(11, 16));
  const data = points.map((item) => Number(item.total || 0));
  const ctx = canvasEl.getContext("2d");

  if (charts.timeline) charts.timeline.destroy();

  charts.timeline = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: text("events", "Events"),
          data,
          borderColor: "rgba(125, 211, 246, 0.8)",
          backgroundColor: "rgba(125, 211, 246, 0.12)",
          borderWidth: 2,
          fill: true,
          pointRadius: 4,
          pointBackgroundColor: "rgba(125, 211, 246, 0.8)",
          pointBorderColor: "rgba(20, 30, 50, 0.95)",
          pointBorderWidth: 2,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: true, labels: { color: "rgba(255, 255, 255, 0.7)" } },
      },
      scales: {
        x: {
          ticks: { color: "rgba(255, 255, 255, 0.6)" },
          grid: { color: "rgba(255, 255, 255, 0.08)" },
        },
        y: {
          ticks: { color: "rgba(255, 255, 255, 0.6)" },
          grid: { color: "rgba(255, 255, 255, 0.08)" },
          beginAtZero: true,
        },
      },
    },
  });
}

function renderTopCves(rows) {
  const container = document.getElementById("top-cves");
  if (!rows?.length) {
    container.innerHTML = `<div class="stack-item">${escapeHtml(text("noCves", "No CVE-linked alerts observed yet."))}</div>`;
    return;
  }

  container.innerHTML = rows
    .map(
      (row) => `
        <article class="stack-item">
          <div class="row">
            <strong>${escapeHtml(row.cve_id)}</strong>
            <span>CVSS ${escapeHtml(row.score ?? "n/a")}</span>
          </div>
          <small>${escapeHtml(text("cveOccurrences", "Occurrences"))}: ${escapeHtml(row.total)}</small>
        </article>
      `
    )
    .join("");
}

function renderStatusSummary(overview) {
  const container = document.getElementById("status-summary");
  const topSource = overview.top_sources?.[0];
  const topRule = overview.status.rule_hits?.[0];
  const rows = [
    [text("lastIngest", "Last ingest"), formatDateTime(overview.last_ingest_at)],
    [text("monitoredSources", "Monitored sources"), (overview.top_sources || []).length],
    [text("topSource", "Top source"), topSource ? `${topSource.source} (${topSource.total})` : text("notAvailable", "n/a")],
    [text("topRule", "Top rule"), topRule ? `${topRule.rule_name} (${topRule.total_hits})` : text("notAvailable", "n/a")],
  ];

  container.innerHTML = rows
    .map(
      ([label, value]) => `
        <div class="summary-card">
          <div class="row">
            <strong>${escapeHtml(label)}</strong>
            <span>${escapeHtml(value)}</span>
          </div>
        </div>
      `
    )
    .join("");
}

async function loadOverview() {
  const overview = await request("/api/overview");
  state.lastOverview = overview;
  renderMetrics(overview);
  renderRuleHits(overview.status.rule_hits || []);
  renderLatestAlerts(overview.latest_alerts || []);
  renderLatestEvents(overview.latest_events || []);
  renderTopIps(overview.top_ips || []);
  renderTimeline(overview.timeline || []);
  renderTopCves(overview.top_cves || []);
  renderStatusSummary(overview);
  updateConsoleHeader(overview);
}

function overviewNeedsBootstrap(overview) {
  return (
    Number(overview?.status?.events_total || 0) === 0 &&
    Number(overview?.status?.active_alerts || 0) === 0 &&
    Number(overview?.status?.critical_alerts || 0) === 0 &&
    (!overview?.latest_events || overview.latest_events.length === 0) &&
    (!overview?.latest_alerts || overview.latest_alerts.length === 0)
  );
}

async function ensureDemoBootstrap() {
  try {
    const overview = await request("/api/overview");
    if (!overviewNeedsBootstrap(overview)) {
      state.lastOverview = overview;
      renderMetrics(overview);
      renderRuleHits(overview.status.rule_hits || []);
      renderLatestAlerts(overview.latest_alerts || []);
      renderLatestEvents(overview.latest_events || []);
      renderTopIps(overview.top_ips || []);
      renderTimeline(overview.timeline || []);
      renderTopCves(overview.top_cves || []);
      renderStatusSummary(overview);
      updateConsoleHeader(overview);
      return;
    }

    await request("/api/demo/bootstrap");
    pushToast(text("demoLoaded", "Demo data loaded for the live console."), "success");
  } catch (error) {
    pushToast(error.message, "error");
  }
}

async function loadAlerts() {
  const status = document.getElementById("alert-status-filter").value;
  const severity = document.getElementById("alert-severity-filter").value;
  const query = new URLSearchParams();
  if (status) query.set("status", status);
  if (severity) query.set("severity", severity);
  const payload = await request(`/api/alerts?${query.toString()}`);
  const rows = payload.rows || [];
  renderAlertsSummary(rows);
  document.getElementById("alerts-table").innerHTML = rows
    .map(
      (row) => `
        <tr>
          <td>${severityBadge(row.severity)}</td>
          <td>${escapeHtml(row.rule_name)}</td>
          <td>${escapeHtml(row.message)}</td>
          <td>${escapeHtml(row.status)}</td>
          <td>${escapeHtml(formatDateTime(row.created_at))}</td>
          <td>
            <button class="table-action" type="button" data-action="ack" data-id="${row.id}">${escapeHtml(text("acknowledge", "Ack"))}</button>
            <button class="table-action" type="button" data-action="resolve" data-id="${row.id}">${escapeHtml(text("resolve", "Resolve"))}</button>
          </td>
        </tr>
      `
    )
    .join("");
}

async function loadEvents() {
  const search = document.getElementById("event-search").value;
  const severity = document.getElementById("event-severity-filter").value;
  const source = document.getElementById("event-source-filter").value;
  const query = new URLSearchParams();
  if (search) query.set("search", search);
  if (severity) query.set("severity", severity);
  const payload = await request(`/api/events?${query.toString()}`);
  const allRows = payload.rows || [];
  renderEventSourceOptions(allRows);
  const rows = allRows.filter((row) => !source || row.source === source);
  renderEventsSummary(rows);
  document.getElementById("events-table").innerHTML = rows
    .map(
      (row) => `
        <tr>
          <td>${escapeHtml(row.event_type)}</td>
          <td>${escapeHtml(row.source)}</td>
          <td>${escapeHtml(row.title)}</td>
          <td>${severityBadge(row.severity)}</td>
          <td>${escapeHtml(formatDateTime(row.created_at))}</td>
        </tr>
      `
    )
    .join("");
}

async function loadStatus() {
  const payload = await request("/api/overview");
  document.getElementById("status-json").textContent = JSON.stringify(payload.status, null, 2);
}

async function loadLanguage(language) {
  state.language = language;
  state.dictionary = await request(`/assets/i18n/${language}.json`);
  applyTranslations();
  applyUiPreferences();
  if (state.lastOverview) {
    renderMetrics(state.lastOverview);
    renderRuleHits(state.lastOverview.status.rule_hits || []);
    renderLatestAlerts(state.lastOverview.latest_alerts || []);
    renderLatestEvents(state.lastOverview.latest_events || []);
    renderTopIps(state.lastOverview.top_ips || []);
    renderTimeline(state.lastOverview.timeline || []);
    renderTopCves(state.lastOverview.top_cves || []);
    renderStatusSummary(state.lastOverview);
    updateConsoleHeader(state.lastOverview);
  }
  updateClock();
}

function installAutoRefresh() {
  if (state.autoRefreshHandle) clearInterval(state.autoRefreshHandle);
  state.autoRefreshHandle = window.setInterval(async () => {
    await refreshAll(true);
  }, REFRESH_INTERVAL_MS);
}

function buildPresetButtons() {
  const container = document.getElementById("ingest-presets");
  container.innerHTML = ingestPresets
    .map(
      (preset, index) => `
        <button type="button" class="preset-btn" data-preset-index="${index}">${escapeHtml(preset.event_type)}</button>
      `
    )
    .join("");

  container.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    const preset = ingestPresets[Number(button.dataset.presetIndex)];
    if (!preset) return;
    const form = document.getElementById("ingest-form");
    Object.entries(preset).forEach(([key, value]) => {
      const field = form.elements.namedItem(key);
      if (field) field.value = value;
    });
  });
}

async function refreshAll(silent = false) {
  try {
    await Promise.all([loadOverview(), loadAlerts(), loadEvents(), loadStatus()]);
    if (!silent) pushToast(text("consoleRefreshed", "Console refreshed successfully."), "success");
  } catch (error) {
    if (!silent) pushToast(error.message, "error");
    throw error;
  }
}

function bindEvents() {
  document.querySelectorAll(".nav-item").forEach((item) =>
    item.addEventListener("click", () => {
      setView(item.dataset.view);
    })
  );

  document.getElementById("global-refresh").addEventListener("click", () => refreshAll());
  document.getElementById("reload-alerts").addEventListener("click", loadAlerts);
  document.getElementById("reload-events").addEventListener("click", loadEvents);
  document.getElementById("alert-status-filter").addEventListener("change", loadAlerts);
  document.getElementById("alert-severity-filter").addEventListener("change", loadAlerts);
  document.getElementById("event-search").addEventListener("input", loadEvents);
  document.getElementById("event-severity-filter").addEventListener("change", loadEvents);
  document.getElementById("event-source-filter").addEventListener("change", loadEvents);

  document.getElementById("language-switcher").addEventListener("change", (event) => loadLanguage(event.target.value));
  document.getElementById("theme-switcher").addEventListener("change", (event) => {
    state.theme = event.target.value;
    applyUiPreferences();
  });
  document.getElementById("density-switcher").addEventListener("change", (event) => {
    state.density = event.target.value;
    applyUiPreferences();
  });
  document.getElementById("contrast-toggle").addEventListener("click", () => {
    state.highContrast = !state.highContrast;
    applyUiPreferences();
  });
  document.getElementById("motion-toggle").addEventListener("click", () => {
    state.reduceMotion = !state.reduceMotion;
    applyUiPreferences();
  });

  document.getElementById("alerts-table").addEventListener("click", async (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    const action = button.dataset.action;
    const id = button.dataset.id;
    const endpoint = action === "resolve" ? "resolve" : "acknowledge";
    try {
      await request(`/api/alerts/${id}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ actor: "dashboard-operator" }),
      });
      pushToast(text("alertActionSuccess", "Alert updated successfully."), "success");
      await refreshAll(true);
    } catch (error) {
      pushToast(error.message, "error");
    }
  });

  document.getElementById("ingest-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = Object.fromEntries(form.entries());
    payload.tags = ["demo", "dashboard"];
    try {
      const result = await request("/api/events/ingest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      document.getElementById("ingest-result").textContent =
        `${text("eventProcessed", "Event processed")}: ${result.event_id}. ` +
        `${text("alertsTriggered", "Alerts triggered")}: ${result.alert_ids.length}`;
      pushToast(text("ingestSuccess", "Sample event ingested successfully."), "success");
      event.currentTarget.reset();
      await refreshAll(true);
    } catch (error) {
      pushToast(error.message, "error");
    }
  });
}

async function bootstrap() {
  readStoredPreferences();
  const config = await request("/api/config");
  document.getElementById("tagline").textContent = config.tagline;
  state.theme = state.theme || config.default_theme || "dark";
  state.language = state.language || config.default_language || "en";
  applyUiPreferences();
  await loadLanguage(state.language);
  buildPresetButtons();
  bindEvents();
  await ensureDemoBootstrap();
  await refreshAll(true);
  installAutoRefresh();
  updateClock();
  window.setInterval(updateClock, 1000);

  revealApp();
}

bootstrap().catch((error) => {
  console.error(error);
  pushToast(error.message, "error");
  revealApp();
});
